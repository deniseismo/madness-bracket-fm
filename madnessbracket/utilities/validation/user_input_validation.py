from typing import Optional

from pydantic import ValidationError, BaseModel, constr
from werkzeug.datastructures import ImmutableMultiDict, MultiDict

from madnessbracket.schemas.input import LastFMUserInput, ArtistUserInput, ArtistsBattleUserInput
from madnessbracket.utilities.validation.exceptions.validation_exceptions import LastFMUserInputError, \
    ArtistUserInputError, ArtistsBattleUserInputError, BracketUpperLimitError
from madnessbracket.utilities.validation.validation_models import LastFMUsername, BracketUpperLimit, ArtistName


def validate_lastfm_user_input(user_input: ImmutableMultiDict | MultiDict[str, str]) -> Optional[LastFMUserInput]:
    """
    validate user input for lastfm user handlers (username, bracket upper limit)
    :param user_input: (ImmutableMultiDict) user's input with username and bracket limit
    :return: (LastFMUserInput) validated user input
    """
    if not isinstance(user_input, ImmutableMultiDict):
        raise LastFMUserInputError("incorrect input type")

    lastfm_username = user_input.get("name")
    bracket_upper_limit = user_input.get("limit")
    if not lastfm_username:
        raise LastFMUserInputError("no username provided")
    if not bracket_upper_limit:
        raise LastFMUserInputError("no bracket limit provided")
    try:
        valid_lastfm_username = LastFMUsername(name=lastfm_username).name
        valid_bracket_upper_limit = BracketUpperLimit(limit=bracket_upper_limit).limit
        return LastFMUserInput(name=valid_lastfm_username, limit=valid_bracket_upper_limit)
    except ValidationError as e:
        print(e.json())
        raise LastFMUserInputError("incorrect username")


def validate_artist_user_input(user_input: ImmutableMultiDict | MultiDict[str, str]) -> Optional[ArtistUserInput]:
    """
    validate user input for artist/musician handlers (artist's name, bracket upper limit)
    :param user_input: (ImmutableMultiDict) user's input with artist's name and bracket limit
    :return: (ArtistUserInput) validated user input
    """
    if not isinstance(user_input, ImmutableMultiDict):
        raise ArtistUserInputError("incorrect input type")
    artist_name = user_input.get("name")
    bracket_upper_limit = user_input.get("limit")
    if not artist_name:
        raise ArtistUserInputError("no artist provided")
    if not bracket_upper_limit:
        raise ArtistUserInputError("no bracket limit provided")

    try:
        valid_artist_name = ArtistName(name=artist_name).name
        valid_bracket_upper_limit = BracketUpperLimit(limit=bracket_upper_limit).limit
        return ArtistUserInput(name=valid_artist_name, limit=valid_bracket_upper_limit)
    except ValidationError as e:
        print(e.json())
        raise ArtistUserInputError("incorrect artist name")


def validate_artists_battle_user_input(user_input: ImmutableMultiDict | MultiDict[str, str]) -> Optional[ArtistsBattleUserInput]:
    """
    validate user input for artists battle (artists names, bracket limit)
    :param user_input: (ImmutableMultiDict) user's input with artists names and bracket limit
    :return: (ArtistsBattleUserInput) validated user input
    """
    if not isinstance(user_input, ImmutableMultiDict):
        raise ArtistUserInputError("incorrect input type")
    artist_name = user_input.get("name")
    artist_2_name = user_input.get("name2")
    bracket_upper_limit = user_input.get("limit")
    if not artist_name or not artist_2_name:
        raise ArtistsBattleUserInputError("no artist provided")
    if not bracket_upper_limit:
        raise ArtistsBattleUserInputError("no bracket limit provided")

    try:
        valid_artist_name = ArtistName(name=artist_name).name
        valid_artist_2_name = ArtistName(name=artist_2_name).name
        valid_bracket_upper_limit = BracketUpperLimit(limit=bracket_upper_limit).limit
        if valid_artist_name.lower() == valid_artist_2_name.lower():
            raise ArtistsBattleUserInputError("IT TAKES TWO TO BATTLE")
        return ArtistsBattleUserInput(name=valid_artist_name, name2=valid_artist_2_name,
                                      limit=valid_bracket_upper_limit)
    except ValidationError as e:
        print(e.json())
        raise ArtistsBattleUserInputError("incorrect artist name")


def validate_bracket_upper_limit(user_input: ImmutableMultiDict | MultiDict[str, str]) -> Optional[int]:
    """
    validate bracket upper limit
    :param user_input: (ImmutableMultiDict) user's input with bracket upper limit
    :return: (int) validated bracket upper limit
    """
    if not isinstance(user_input, ImmutableMultiDict):
        raise BracketUpperLimitError("incorrect input type")
    bracket_upper_limit = user_input.get("limit")
    if not bracket_upper_limit:
        raise BracketUpperLimitError("no bracket limit provided")

    try:
        valid_bracket_upper_limit = BracketUpperLimit(limit=bracket_upper_limit).limit
        return valid_bracket_upper_limit
    except ValidationError as e:
        print(e.json())
        raise BracketUpperLimitError("incorrect bracket upper limit")


def is_valid_nanoid(bracket_id_to_check):
    """checks if a given string is a valid nanoid string

        Args:
            bracket_id_to_check (str): bracket's ID

        Returns:
            (bool): true if valid, false otherwise
    """

    class BracketID(BaseModel):
        bracket_id: constr(regex=r'[A-Za-z0-9_-]{13}')

    try:
        user_input = BracketID(bracket_id=bracket_id_to_check)
        return True
    except ValidationError as e:
        print(e.json())
        print('incorrect bracket id')
        return False