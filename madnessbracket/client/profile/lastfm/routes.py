import json

from flask import Blueprint, jsonify, request, make_response, render_template

from madnessbracket.profile.lastfm.lastfm_profile_handlers import ultimate_lastfm_user_tracks_handler
from madnessbracket.utilities.validation.exceptions.validation_exceptions import LastFMUserInputError
from madnessbracket.utilities.validation.user_input_validation import validate_lastfm_user_input

lastfm_profile = Blueprint('lastfm_profile', __name__)


@lastfm_profile.route('/lastfm', methods=["GET", "POST"])
def generate_lastfm_user_bracket():
    """generates USER's personal bracket based on their LAST.FM stats
    Returns:
        jsonified dict with all the tracks and tracks' info needed for the bracket
    """
    try:
        valid_user_input = validate_lastfm_user_input(request.args)
        lastfm_username = valid_user_input.name
        bracket_upper_limit = valid_user_input.limit
    except LastFMUserInputError as e:
        if request.method == "GET":
            return render_template('404.html', description='👿 INCORRECT INPUT 👿'), 404
        else:
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
        tracks = ultimate_lastfm_user_tracks_handler(lastfm_username, bracket_upper_limit)
        print(tracks)
        if not tracks:
            print('nothing found')
            return make_response(jsonify(
                {'message': f"😟 no tracks found for {lastfm_username} 😟"}
            ),
                404)
        return jsonify(tracks)
