from flask import Blueprint, jsonify, request, make_response

from madnessbracket.musician.musician_handlers import get_artists_tracks
from madnessbracket.musician.prepare_tracks import prepare_tracks_for_musician
musician = Blueprint('musician', __name__)


@musician.route('/artist', methods=['POST'])
def generate_musician_bracket():
    """generates madness bracket for a particular artist/musician
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
        # get chosen bracket upper limit
        bracket_limit = int(content['limit'])
        # get chosen artist's name
        artist_name = content['value']
    except (KeyError, ValueError, TypeError):
        print('bogus input')
        return make_response(jsonify(
            {'message': f"something's gone wrong"}
        ),
            404)
    tracks = get_artists_tracks(artist_name, bracket_limit)
    print(tracks)
    if not tracks:
        print('nothing found')
        return make_response(jsonify(
            {'message': f"no tracks found for {artist_name}"}
        ),
            404)
    return jsonify(tracks)
