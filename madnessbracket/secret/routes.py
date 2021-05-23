import json

from flask import Blueprint, jsonify, request, make_response, render_template

from madnessbracket.secret.secret_handlers import get_secret_tracks
from madnessbracket.utilities.user_input_validation import validate_bracket_upper_limit

secret = Blueprint('secret', __name__)


@secret.route('/secret', methods=['POST', "GET"])
def generate_secret_bracket():
    """generates SECRET madness bracket
    Returns:
        jsonified dict with all the tracks and tracks' info needed for the bracket
    """
    upper_limit = request.args.get("limit")
    valid_upper_limit = validate_bracket_upper_limit(upper_limit)
    if request.method == "GET":
        if not valid_upper_limit:
            return render_template('404.html', description='👿 INCORRECT INPUT 👿'), 404
        user_request = json.dumps({
            "bracket_type": "secret",
            "name": None,
            "limit": upper_limit
        })
        return render_template("bracket.html", user_request=user_request)

    else:
        if not valid_upper_limit:
            print('incorrect input')
            return make_response(jsonify(
                {'message': f'👿 INCORRECT INPUT 👿'}
            ),
                404)
        upper_limit = valid_upper_limit.upper_limit
        tracks = get_secret_tracks(upper_limit)
        print(tracks)
        if not tracks:
            print('nothing found')
            return make_response(jsonify(
                {'message': f"😟 NOTHING FOUND 😟"}
            ),
                404)
        return jsonify(tracks)
