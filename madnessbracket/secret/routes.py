from flask import Blueprint, jsonify, request, make_response
from madnessbracket.secret.secret_handlers import get_secret_tracks

secret = Blueprint('secret', __name__)


@secret.route('/secret', methods=['POST'])
def generate_musician_bracket():
    """generates madness bracket for the best/classics/charts type of tracks
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
    except (KeyError, ValueError, TypeError):
        print('bogus input')
        return make_response(jsonify(
            {'message': f"something's gone wrong"}
        ),
            404)
    tracks = get_secret_tracks(bracket_limit)
    print(tracks)
    if not tracks:
        print('nothing found')
        return make_response(jsonify(
            {'message': f"nothing found"}
        ),
            404)
    return jsonify(tracks)
