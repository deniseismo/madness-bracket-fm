import json
import pickle

import tekore as tk
from flask import request, url_for, Blueprint, redirect, session, make_response, jsonify, render_template, flash, \
    Response

from madnessbracket.client.database_manipulation.db_user_handlers import add_new_spotify_user_to_database
from madnessbracket.client.profile.spotify.spotify_profile_handlers import get_tracks_for_spotify_user
from madnessbracket.music_apis.spotify_api.spotify_user_handlers import get_spotify_auth, authenticate_spotify_user
from madnessbracket.models import User
from madnessbracket.music_apis.spotify_api.spotify_client_api import get_spotify_tekore_client
from madnessbracket.track_processing.track_processing_helpers import make_tracks_info_response
from madnessbracket.utilities.validation.exceptions.validation_exceptions import BracketUpperLimitError
from madnessbracket.utilities.validation.user_input_validation import validate_bracket_upper_limit

spotify = Blueprint('spotify', __name__)


@spotify.route("/spotify_login", methods=['GET'])
def spotify_login():
    """
    get an authorization url and redirects to the spotify login page
    :return: redirect url
    """
    auth = get_spotify_auth()
    # store a random state in a server-side cookie-session
    session['state'] = auth.state
    return redirect(auth.url, 307)


@spotify.route('/spotify_logout', methods=['POST'])
def spotify_logout():
    """
    logs user out
    :return: redirects to the home page
    """
    user = session.pop('user', None)
    flash(f"😈 you've logged out 😈", "info")
    return redirect(url_for('main.home'), 307)


@spotify.route("/spotify_callback", methods=["GET"])
def spotify_callback():
    """
    a function that gets triggered after the user successfully granted the permission
    """
    error = request.args.get('error', None)
    code = request.args.get('code', None)
    state = request.args.get('state', None)
    if error:
        flash(f"😟 you haven't logged in 😟", "warning")
        return redirect(url_for('main.home'), 307)

    # get current user's state
    user_state = session.get('state', None)
    # check if it's there and equals to the state from the callback (against cross-site forgery)
    if user_state is None or user_state != state:
        flash(f"😟 you haven't logged in 😟", "warning")
        return redirect(url_for('main.home'), 307)

    auth = get_spotify_auth()
    # get token object (Tekore token with access and refresh token inside)
    token = auth.request_token(code, auth.state)

    # put serialized token in a session
    session['token'] = pickle.dumps(token)
    spotify_tekore_client = get_spotify_tekore_client()
    if not spotify_tekore_client:
        return None
    try:
        with spotify_tekore_client.token_as(token):
            current_user = spotify_tekore_client.current_user()
            spotify_user_id = current_user.id
            # put user's id in a session
            session['user'] = spotify_user_id
            user_entry = User.query.filter_by(spotify_id=spotify_user_id).first()
            if not user_entry:
                print(f'New Spotify User({spotify_user_id})!')
                add_new_spotify_user_to_database(spotify_user_id, token.refresh_token)

    except tk.HTTPError:
        flash(f"😟 we're sorry, but you've failed to log in 😟", "error")
        return None
    return redirect(url_for('spotify.generate_spotify_bracket'), 307)


@spotify.route('/spotify', methods=["GET", "POST"])
def generate_spotify_bracket() -> Response:
    """
    generates madness bracket based on spotify's user best tracks
    :return: jsonified dict with all the needed info for the madness bracket
    """
    try:
        bracket_upper_limit = validate_bracket_upper_limit(request.args)
    except BracketUpperLimitError as e:
        return make_response(jsonify(
            {'message': f'👿 INCORRECT INPUT 👿'}
        ),
            404)
    user, token = authenticate_spotify_user()
    if not user or not token:
        return make_response(jsonify(
            {'message': f"👿 YOU'RE NOT LOGGED IN 👿"}
        ),
            404)
    if request.method == "GET":
        user_request = json.dumps({
            "bracket_type": "spotify",
            "limit": bracket_upper_limit
        })
        return render_template("bracket.html", user_request=user_request)
    else:
        spotify_user_tracks_info = get_tracks_for_spotify_user(token, bracket_upper_limit)
        if not spotify_user_tracks_info:
            return make_response(jsonify(
                {'message': f"😟 no tracks found for you 😟"}
            ),
                404)
        tracks_info_response = make_tracks_info_response(
            tracks=spotify_user_tracks_info.tracks,
            description=f"{spotify_user_tracks_info.username}: My Spotify",
            extra=None
        )
        return jsonify(tracks_info_response)
