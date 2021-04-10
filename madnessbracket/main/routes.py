from flask import render_template, Blueprint, jsonify, request, make_response
from madnessbracket.spotify_api.get_users_fav_tracks import get_users_favorite_tracks
from madnessbracket.utilities.track_processing import cap_tracks
from madnessbracket.charts.get_top_rated_tracks import get_top_rated_songs
from madnessbracket.musician.get_artists_tracks import get_artists_tracks
main = Blueprint('main', __name__)


@main.route("/", methods=["GET", "POST"])
@main.route("/home", methods=["GET", "POST"])
def home():
    """renders home page

    Returns:
        home page template (home.html)
    """
    return render_template("home.html")


@main.route('/bracket', methods=['POST'])
def generate_bracket():
    """generates madness bracket depending on user's input/selected options
    Returns:
        jsonified dict with all the tracks and tracks' info needed for the bracket
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
        # get all the needed info from the user
        tracks_type = content['type']
        bracket_limit = int(content['limit'])
        # input value's used only for artist/musician
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
    elif tracks_type == "charts":
        print('best songs mode')
        tracks = get_top_rated_songs()
        print(tracks)
    # get artist's top tracks
    elif tracks_type == "artist":
        print(input_value)
        print('artist mode')
        tracks = get_artists_tracks(input_value)
    else:
        print('bogus tracks type:', tracks_type)
        return make_response(jsonify(
            {'message': f"something's gone wrong"}
        ),
            404)
    if not tracks:
        print('nothing found')
        return make_response(jsonify(
            {'message': f"nothing found"}
        ),
            404)
    tracks = cap_tracks(tracks, bracket_limit, tracks_type)
    return jsonify(tracks)
