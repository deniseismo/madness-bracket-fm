import json

from flask import Blueprint, jsonify, request, make_response, render_template

from madnessbracket.client.charts.charts_handlers import get_tracks_for_charts
from madnessbracket.track_processing.track_processing_helpers import make_tracks_info_response
from madnessbracket.utilities.validation.exceptions.validation_exceptions import BracketUpperLimitError
from madnessbracket.utilities.validation.user_input_validation import validate_bracket_upper_limit

charts = Blueprint('charts', __name__)


@charts.route('/charts', methods=['POST', "GET"])
def generate_charts_bracket():
    """
    generates madness bracket with tracks from charts (songs considered best, NME/RS lists of best songs, etc.)
    :return: jsonified dict with all the needed info for the madness bracket
    """
    try:
        bracket_upper_limit = validate_bracket_upper_limit(request.args)
    except BracketUpperLimitError as e:
        return make_response(jsonify(
            {'message': str(e)}
        ),
            404)
    if request.method == "GET":
        user_request = json.dumps({
            "bracket_type": "charts",
            "name": None,
            "limit": bracket_upper_limit
        })
        return render_template("bracket.html", user_request=user_request)
    else:
        charts_tracks = get_tracks_for_charts(bracket_upper_limit)
        if not charts_tracks:
            return make_response(jsonify(
                {'message': f"😟 NO TRACKS FOUND 😟"}
            ),
                404)
        tracks_info_response = make_tracks_info_response(
            tracks=charts_tracks,
            description="CHARTS",
            extra=None
        )
        return jsonify(tracks_info_response)
