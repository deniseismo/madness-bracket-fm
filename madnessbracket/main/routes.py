from flask import render_template, Blueprint, jsonify, request, make_response
from madnessbracket.spotify_api.spotify_user_oauth import check_spotify, get_spotify_user_info
from madnessbracket.spotify_api.get_users_fav_tracks import get_users_favorite_tracks
from madnessbracket.utilities.track_processing import cap_tracks
from madnessbracket.charts.get_top_rated_tracks import get_top_rated_songs
from madnessbracket.musician.get_artists_tracks import get_artists_tracks
main = Blueprint('main', __name__)


@main.route("/", methods=["GET", "POST"])
@main.route("/home", methods=["GET", "POST"])
def home():
    """
    renders home page
    """
    logged_in = False
    user_info = None
    user, token = check_spotify()
    if user and token:
        logged_in = True
        user_info = get_spotify_user_info(token.access_token)
    return render_template("home.html", logged_in=logged_in, user_info=user_info)


@main.route('/bracket', methods=['POST'])
def generate_bracket():
    """
    handles the main routing/logic of the app
    receieves user's input → returns prepared tracks accordingly
    """
    # input's values/options
    content = request.get_json()
    if not content:
        print('no input')
        return make_response(jsonify(
            {'message': f"something's gone wrong"}
        ),
            404)
    try:
        tracks_type = content['type']
        bracket_limit = content['limit']
        input_value = content['value']
    except (KeyError, ValueError, TypeError):
        print('bogus input')
        return make_response(jsonify(
            {'message': f"something's gone wrong"}
        ),
            404)
    # check 'retrieval' method
    # get user's fav tracks via spotify
    if tracks_type == "spotify":
        print('spotify mode')
        tracks = get_users_favorite_tracks()
    # get songs considered best
    elif tracks_type == "best":
        print('best songs mode')
        tracks = get_top_rated_songs()
        print(tracks)
    # get artist's top tracks
    elif tracks_type == "artist":
        print('artist mode')
        tracks = get_artists_tracks(input_value)
    else:
        print('bogus tracks type')
        return make_response(jsonify(
            {'message': f"something's gone wrong"}
        ),
            404)

    tracks = cap_tracks(tracks, bracket_limit)
    return jsonify(tracks)
