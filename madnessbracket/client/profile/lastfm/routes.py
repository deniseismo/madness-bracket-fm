import json

from flask import Blueprint, jsonify, request, make_response, render_template

from madnessbracket.client.profile.lastfm.lastfm_profile_handlers import get_tracks_for_lastfm_user
from madnessbracket.track_processing.track_processing_helpers import make_tracks_info_response
from madnessbracket.utilities.validation.exceptions.validation_exceptions import LastFMUserInputError
from madnessbracket.utilities.validation.user_input_validation import validate_lastfm_user_input

lastfm_profile = Blueprint('lastfm_profile', __name__)


@lastfm_profile.route('/lastfm', methods=["GET", "POST"])
def generate_lastfm_user_bracket():
    """
    generate madness bracket based on lastfm's user listening stats (user's profile on lastfm)
    :return: jsonified dict with all the needed info for the madness bracket
    """
    try:
        valid_user_input = validate_lastfm_user_input(request.args)
        lastfm_username = valid_user_input.name
        bracket_upper_limit = valid_user_input.limit
    except LastFMUserInputError as e:
        return make_response(jsonify(
            {'message': str(e)}
        ),
            404)
    if request.method == "GET":
        user_request = json.dumps({
            "bracket_type": "lastfm",
            "value1": lastfm_username,
            "limit": bracket_upper_limit
        })
        return render_template("bracket.html", user_request=user_request)
    else:
        lastfm_user_tracks_info = get_tracks_for_lastfm_user(lastfm_username, bracket_upper_limit)
        if not lastfm_user_tracks_info:
            print('nothing found')
            return make_response(jsonify(
                {'message': f"😟 no tracks found for {lastfm_username} 😟"}
            ),
                404)
        tracks_info_response = make_tracks_info_response(
            tracks=lastfm_user_tracks_info.tracks,
            description=f"{lastfm_user_tracks_info.username}: My Last.fm",
            value1=lastfm_user_tracks_info.username,
            extra=None
        )
        return jsonify(tracks_info_response)
