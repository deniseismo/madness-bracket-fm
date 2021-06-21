import json
from madnessbracket.battle.artists_battle_handlers import get_artists_battle

from flask import Blueprint, jsonify, request, make_response, render_template

from madnessbracket.utilities.user_input_validation import validate_artist_name, validate_bracket_upper_limit

battle = Blueprint('battle', __name__)


@battle.route('/battle', methods=['POST', "GET"])
def generate_battle_bracket():
    """generates madness bracket for ARTIST BATTLE (e.g. Radiohead vs Muse)
    Returns:
        jsonified dict with all the tracks and tracks' info needed for the bracket
    """
    artist_name = request.args.get("name")
    artist_name_2 = request.args.get("name2")
    upper_limit = request.args.get("limit")
    valid_artist_name = validate_artist_name(artist_name)
    valid_artist_name_2 = validate_artist_name(artist_name_2)
    valid_upper_limit = validate_bracket_upper_limit(upper_limit)
    is_valid_input = valid_artist_name and valid_upper_limit and valid_artist_name_2
    if request.method == "GET":
        if not is_valid_input:
            return render_template('404.html', description='👿 INCORRECT INPUT 👿'), 404

        if artist_name == artist_name_2:
            return render_template('404.html', description='👿 IT TAKES TWO TO BATTLE 👿'), 404

        user_request = json.dumps({
            "bracket_type": "battle",
            "name": artist_name,
            "name2": artist_name_2,
            "limit": upper_limit
        })
        return render_template("bracket.html", user_request=user_request)
    else:
        if not is_valid_input:
            return make_response(jsonify(
                {'message': f'👿 INCORRECT INPUT 👿'}
            ),
                404)
        if artist_name == artist_name_2:
            return make_response(jsonify(
                {'message': f'👿 IT TAKES TWO TO BATTLE 👿'}
            ),
                404)
        upper_limit = valid_upper_limit.upper_limit
        tracks = get_artists_battle(artist_name, artist_name_2, upper_limit)
        if not tracks:
            print('nothing found')
            return make_response(jsonify(
                {'message': f"😟 no tracks found for {artist_name} 😟"}
            ),
                404)
        return jsonify(tracks)
