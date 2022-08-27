import json

from flask import Blueprint, jsonify, request, make_response, render_template, Response

from madnessbracket.client.artist.artist_handlers import get_tracks_for_artist
from madnessbracket.client.artist.fetch_artists_handlers import get_filtered_artists_suggestions
from madnessbracket.music_apis.lastfm_api.lastfm_artist_handlers import lastfm_get_artist_correct_name
from madnessbracket.track_processing.track_processing_helpers import make_tracks_info_response
from madnessbracket.utilities.validation.exceptions.validation_exceptions import ArtistUserInputError
from madnessbracket.utilities.validation.user_input_validation import validate_artist_user_input

artist = Blueprint('artist', __name__)


@artist.route('/artist', methods=['POST', "GET"])
def generate_artist_bracket():
    """generates madness bracket for a particular artist/musician
    Returns:
        jsonified dict with all the tracks and tracks' info needed for the bracket
    """
    try:
        valid_user_input = validate_artist_user_input(request.args)
        artist_name = valid_user_input.name
        bracket_upper_limit = valid_user_input.limit
    except ArtistUserInputError as e:
        return make_response(jsonify(
            {'message': str(e)}
        ),
            404)

    if request.method == "GET":
        user_request = json.dumps({
            "bracket_type": "artist",
            "value1": artist_name,
            "limit": bracket_upper_limit
        })
        return render_template("bracket.html", user_request=user_request)
    else:
        artist_correct_name = lastfm_get_artist_correct_name(artist_name)
        if artist_correct_name:
            artist_name = artist_correct_name
        artist_tracks = get_tracks_for_artist(artist_name, bracket_upper_limit)
        if not artist_tracks:
            return make_response(jsonify(
                {'message': f"😟 no tracks found for {artist_name} 😟"}
            ),
                404)
        tracks_info_response = make_tracks_info_response(
            tracks=artist_tracks,
            description=f"{artist_name.upper()}",
            value1=artist_name,
            extra=None
        )
        return jsonify(tracks_info_response)


@artist.route('/get_artists', methods=['POST'])
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
