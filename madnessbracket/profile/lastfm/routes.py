import json

from flask import Blueprint, jsonify, request, make_response, render_template

from madnessbracket.profile.lastfm.lastfm_profile_handlers import ultimate_lastfm_user_tracks_handler
from madnessbracket.utilities.user_input_validation import validate_bracket_upper_limit, validate_lastfm_username

lastfm_profile = Blueprint('lastfm_profile', __name__)


@lastfm_profile.route('/lastfm', methods=["GET", "POST"])
def generate_lastfm_user_bracket():
    """generates USER's personal bracket based on their LAST.FM stats
    Returns:
        jsonified dict with all the tracks and tracks' info needed for the bracket
    """
    username = request.args.get("name")
    upper_limit = request.args.get("limit")
    valid_username = validate_lastfm_username(username)
    valid_upper_limit = validate_bracket_upper_limit(upper_limit)
    is_valid_input = valid_username and valid_upper_limit
    if request.method == "GET":
        if not is_valid_input:
            return render_template('404.html', description='👿 INCORRECT INPUT 👿'), 404

        user_request = json.dumps({
            "bracket_type": "lastfm",
            "value1": username,
            "limit": upper_limit
        })
        return render_template("bracket.html", user_request=user_request)
    else:
        if not is_valid_input:
            print('no input')
            return make_response(jsonify(
                {'message': f"👿 INCORRECT INPUT 👿"}
            ),
                404)
        upper_limit = valid_upper_limit.upper_limit
        tracks = ultimate_lastfm_user_tracks_handler(username, upper_limit)
        print(tracks)
        if not tracks:
            print('nothing found')
            return make_response(jsonify(
                {'message': f"😟 no tracks found for {username} 😟"}
            ),
                404)
        return jsonify(tracks)
