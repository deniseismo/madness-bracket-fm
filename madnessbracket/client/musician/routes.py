import json

from flask import Blueprint, jsonify, request, make_response, render_template, Response

from madnessbracket.musician.fetch_artists_handlers import get_filtered_artists_suggestions
from madnessbracket.musician.musician_handlers import get_musician_bracket_data
from madnessbracket.utilities.user_input_validation import validate_artist_name, validate_bracket_upper_limit
from madnessbracket.utilities.validation.exceptions.validation_exceptions import ArtistUserInputError
from madnessbracket.utilities.validation.user_input_validation import validate_artist_user_input

musician = Blueprint('musician', __name__)


@musician.route('/artist', methods=['POST', "GET"])
def generate_musician_bracket():
    """generates madness bracket for a particular artist/musician
    Returns:
        jsonified dict with all the tracks and tracks' info needed for the bracket
    """
    try:
        valid_user_input = validate_artist_user_input(request.args)
        valid_artist_name = valid_user_input.name
        valid_bracket_upper_limit = valid_user_input.limit
    except ArtistUserInputError as e:
        if request.method == "GET":
            return render_template('404.html', description='👿 INCORRECT INPUT 👿'), 404
        else:
            return make_response(jsonify(
                {'message': str(e)}
            ),
                404)

    if request.method == "GET":
        user_request = json.dumps({
            "bracket_type": "artist",
            "value1": valid_artist_name,
            "limit": valid_bracket_upper_limit
        })
        return render_template("bracket.html", user_request=user_request)
    else:
        tracks = get_musician_bracket_data(valid_artist_name, valid_bracket_upper_limit)
        print(tracks)
        if not tracks:
            print('nothing found')
            return make_response(jsonify(
                {'message': f"😟 no tracks found for {valid_artist_name} 😟"}
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
