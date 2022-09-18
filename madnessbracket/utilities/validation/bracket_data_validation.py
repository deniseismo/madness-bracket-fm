from typing import Optional

from pydantic import ValidationError

from madnessbracket.utilities.validation.exceptions.validation_exceptions import BracketDataError, \
    WinnerTrackBracketDataError
from madnessbracket.utilities.validation.validation_models import SharedBracketData, WinnerTrackBracketData


def validate_bracket_data(bracket_data: dict) -> Optional[SharedBracketData]:
    """
    validate bracket data (coming from the user) used for sharing madness bracket
    :param bracket_data: (dict) madness bracket data from the user
    """
    if not isinstance(bracket_data, dict):
        raise BracketDataError("incorrect input type")
    try:
        valid_bracket_data = SharedBracketData(**bracket_data)
        return valid_bracket_data
    except ValidationError as e:
        print(e.json())
        raise BracketDataError("incorrect bracket data")


def validate_winner_track_bracket_data(winner_track_bracket_data: dict) -> Optional[WinnerTrackBracketData]:
    """
    validate winner track bracket data (used to generate easter egg commentary/trivia/fun quotes, etc.)
    :param winner_track_bracket_data: (dict) winner track and general bracket info
    """
    if not isinstance(winner_track_bracket_data, dict):
        raise WinnerTrackBracketDataError("incorrect input type")
    try:
        valid_winner_track_bracket_data = WinnerTrackBracketData(**winner_track_bracket_data)
        return valid_winner_track_bracket_data
    except ValidationError as e:
        print(e.json())
        raise WinnerTrackBracketDataError("incorrect winner bracket data")
