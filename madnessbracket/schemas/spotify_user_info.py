from dataclasses import dataclass
from typing import Optional, NamedTuple

from tekore._model import FullTrack

from madnessbracket.schemas.info_base import InfoBase
from madnessbracket.schemas.track_schema import TrackInfo


@dataclass
class SpotifyUserAuth(InfoBase):
    """
    dataclass used to store Spotify user authentication params

    :attr spotify_user_id: (str) spotify user id (unique id on Spotify)
    :attr token: (str) access token
    """
    spotify_user_id: Optional[str] = None
    token: Optional[str] = None


@dataclass
class SpotifyUserProfile(InfoBase):
    """
    dataclass used to store information about Spotify User

    :attr username: (str) spotify username
    :attr country: (str) user's country
    :attr user_image: (str) user's avatar url (if there is one)
    """
    username: str
    country: str = None
    user_image: str = None


class SpotifyTopTracksInfo(NamedTuple):
    """
    dataclass used to store information about spotify user and their tracks
    (unprocessed FullTrack tekore spotify objects)

    :attr username: (str) spotify username
    :attr tracks: (list[FullTrack]) list of user's top tracks  (unprocessed FullTrack tekore spotify objects)
    """
    username: str
    tracks: list[FullTrack]


@dataclass
class SpotifyTopTracksProcessedInfo(InfoBase):
    """
    dataclass used to store information about spotify user and their tracks (processed & ready for madness bracket)

    :attr username: (str) spotify username
    :attr tracks: (list[TrackInfo]) list of user's top tracks (processed as TrackInfo objects)
    """
    username: str
    tracks: list[TrackInfo]