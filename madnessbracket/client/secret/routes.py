import json

from flask import Blueprint, jsonify, request, make_response, render_template

from madnessbracket.client.secret.secret_handlers import get_tracks_for_secret
from madnessbracket.utilities.validation.exceptions.validation_exceptions import BracketUpperLimitError
from madnessbracket.utilities.validation.user_input_validation import validate_bracket_upper_limit

secret = Blueprint('secret', __name__)


@secret.route('/secret', methods=['POST', "GET"])
def generate_secret_bracket():
    """
    generates secret madness bracket
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
            "bracket_type": "secret",
            "name": None,
            "limit": bracket_upper_limit
        })
        return render_template("bracket.html", user_request=user_request)

    else:
        secret_tracks_info = get_tracks_for_secret(bracket_upper_limit)
        if not secret_tracks_info:
            return make_response(jsonify(
                {'message': f"😟 NOTHING FOUND 😟"}
            ),
                404)
        return jsonify(secret_tracks_info)
