from dataclasses import dataclass

from madnessbracket.schemas.info_base import InfoBase
from madnessbracket.schemas.track_schema import TrackInfo


@dataclass
class TracksInfoResponse(InfoBase):
    """

    dataclass used to represent main response that will be returned to the user

    :attr tracks: (list[TrackInfo]) all the information about tracks
    :attr description: (str) all the information about albums & album covers returned to the user
    :attr value1: (str) 'main name/character in question' (e.g. artist's name, user's name, etc.)
    :attr value2: (str) artist's name (can be used in artists battles where two artists are present)
    :attr extra: (str) extra information about the bracket type if needed (e.g. 'secret', 'battle');
        can be used on frontend for different behaviour
    """
    tracks: list[TrackInfo]
    description: str
    value1: str = None
    value2: str = None
    extra: str = None
