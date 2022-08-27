import json

from flask import Blueprint, jsonify, request, make_response, render_template

from madnessbracket.client.battle.artists_battle_handlers import get_tracks_for_artists_battle
from madnessbracket.music_apis.lastfm_api.lastfm_artist_handlers import lastfm_get_artist_correct_name
from madnessbracket.track_processing.track_processing_helpers import make_tracks_info_response
from madnessbracket.utilities.validation.exceptions.validation_exceptions import ArtistsBattleUserInputError
from madnessbracket.utilities.validation.user_input_validation import validate_artists_battle_user_input

battle = Blueprint('battle', __name__)


@battle.route('/battle', methods=['POST', "GET"])
def generate_battle_bracket():
    """
    generates madness bracket for artists battle (e.g. The Stone Roses vs Oasis)
    :return: jsonified dict with all the needed info for the madness bracket
    """
    try:
        valid_user_input = validate_artists_battle_user_input(request.args)
        artist_1_name = valid_user_input.name
        artist_2_name = valid_user_input.name2
        bracket_upper_limit = valid_user_input.limit
    except ArtistsBattleUserInputError as e:
        return make_response(jsonify(
            {'message': str(e)}
        ),
            404)

    if request.method == "GET":
        user_request = json.dumps({
            "bracket_type": "battle",
            "value1": artist_1_name,
            "value2": artist_2_name,
            "limit": bracket_upper_limit
        })
        return render_template("bracket.html", user_request=user_request)
    else:
        artist_1_correct_name = lastfm_get_artist_correct_name(artist_1_name)
        if artist_1_correct_name:
            artist_1_name = artist_1_correct_name
        artist_2_correct_name = lastfm_get_artist_correct_name(artist_2_name)
        if artist_2_correct_name:
            artist_2_name = artist_2_correct_name
        battle_tracks = get_tracks_for_artists_battle(artist_1_name, artist_2_name, bracket_upper_limit)
        if not battle_tracks:
            return make_response(jsonify(
                {'message': f"😟 NO TRACKS FOUND FOR THIS BATTLE 😟"}
            ),
                404)
        tracks_info_response = make_tracks_info_response(
            tracks=battle_tracks,
            description=f"{artist_1_name.upper()} vs {artist_2_name.upper()}",
            value1=artist_1_name,
            value2=artist_2_name,
            extra="artists_battle"
        )
        return jsonify(tracks_info_response)
