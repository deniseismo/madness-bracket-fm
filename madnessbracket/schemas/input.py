from typing import NamedTuple


class LastFMUserInput(NamedTuple):
    """
    """
    name: str
    limit: int


class ArtistUserInput(NamedTuple):
    """
    """
    name: str
    limit: int


class ArtistsBattleUserInput(NamedTuple):
    """
    """
    name: str
    name2: str
    limit: int
