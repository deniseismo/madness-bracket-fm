import json

from flask import Blueprint, jsonify, request, make_response, render_template, Response

from madnessbracket.musician.fetch_artists_handlers import get_filtered_artists_suggestions
from madnessbracket.musician.musician_handlers import get_musician_bracket_data
from madnessbracket.utilities.user_input_validation import validate_artist_name, validate_bracket_upper_limit

musician = Blueprint('musician', __name__)


@musician.route('/artist', methods=['POST', "GET"])
def generate_musician_bracket():
    """generates madness bracket for a particular artist/musician
    Returns:
        jsonified dict with all the tracks and tracks' info needed for the bracket
    """
    artist_name = request.args.get("name")
    upper_limit = request.args.get("limit")
    valid_artist_name = validate_artist_name(artist_name)
    valid_upper_limit = validate_bracket_upper_limit(upper_limit)
    is_valid_input = valid_artist_name and valid_upper_limit
    if request.method == "GET":
        if not is_valid_input:
            return render_template('404.html', description='👿 INCORRECT INPUT 👿'), 404

        user_request = json.dumps({
            "bracket_type": "artist",
            "value1": artist_name,
            "limit": upper_limit
        })
        return render_template("bracket.html", user_request=user_request)
    else:
        if not is_valid_input:
            print('no input')
            return make_response(jsonify(
                {'message': f'👿 INCORRECT INPUT 👿'}
            ),
                404)
        upper_limit = valid_upper_limit.upper_limit
        tracks = get_musician_bracket_data(artist_name, upper_limit)
        print(tracks)
        if not tracks:
            print('nothing found')
            return make_response(jsonify(
                {'message': f"😟 no tracks found for {artist_name} 😟"}
            ),
                404)
        return jsonify(tracks)


@musician.route('/get_artists', methods=['POST'])
def get_artists() -> Response:
    """
    gets a list of artists
    filtered based on the search query
    :return:
    """
    suggestions = {"suggestions": []}
    try:
        search_query = request.get_json()['query']
    except (KeyError, TypeError, IndexError):
        return jsonify(suggestions)
    if not search_query:
        return jsonify(suggestions)
    search_query = search_query.lower()
    # check if the input's not empty
    suggestions["suggestions"] = get_filtered_artists_suggestions(search_query)
    return jsonify(suggestions)
