from flask import Blueprint, jsonify, request, make_response
from madnessbracket.charts.prepare_tracks import prepare_tracks_for_charts
from madnessbracket.charts.charts_handlers import get_songs_considered_best
charts = Blueprint('charts', __name__)


@charts.route('/charts', methods=['POST'])
def generate_charts_bracket():
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
    except (KeyError, ValueError, TypeError):
        print('bogus input')
        return make_response(jsonify(
            {'message': f"something's gone wrong"}
        ),
            404)
    tracks = get_songs_considered_best()
    print(tracks)
    if not tracks:
        print('nothing found')
        return make_response(jsonify(
            {'message': f"nothing found"}
        ),
            404)
    tracks = prepare_tracks_for_charts(tracks, bracket_limit)
    return jsonify(tracks)
