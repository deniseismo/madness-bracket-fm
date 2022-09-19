from flask import request, Blueprint, jsonify, Response

from madnessbracket.client.trivia.commentary_generator import CommentaryGenerator
from madnessbracket.utilities.logging_handlers import log_winner_track
from madnessbracket.utilities.validation.bracket_data_validation import validate_winner_track_bracket_data
from madnessbracket.utilities.validation.exceptions.validation_exceptions import WinnerTrackBracketDataError

trivia = Blueprint('trivia', __name__)


@trivia.route("/get_commentary", methods=["POST"])
def get_madness_commentary() -> Response:
    """
    get madness bracket commentary: easter egg commentary for the madness bracket winner track
    :return: jsonified commentary info
    """
    winner_track_bracket_data = request.get_json()
    # validate bracket data via pydantic models
    try:
        validated_winner_track_bracket_data = validate_winner_track_bracket_data(winner_track_bracket_data)
    except WinnerTrackBracketDataError as e:
        return jsonify({
            "commentary": None
        })
    artist_name = validated_winner_track_bracket_data.artist_name
    song_title = validated_winner_track_bracket_data.song_title
    log_winner_track(
        artist_name,
        song_title,
        validated_winner_track_bracket_data.bracket_type,
        validated_winner_track_bracket_data.description
    )
    commentary = CommentaryGenerator(song_title=song_title, artist_name=artist_name).get_commentary()
    return jsonify({
        "commentary": commentary
    })
