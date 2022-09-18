from dataclasses import dataclass
from typing import NamedTuple

from madnessbracket.schemas.info_base import InfoBase
from madnessbracket.schemas.track_schema import TrackInfo


class LastFMUserTopTracksInfo(NamedTuple):
    """
    namedtuple used to store information about lastfm user and their tracks

    :attr username: (str) lastfm username
    :attr tracks: (list[dict[str]]) user's top tracks
    """
    username: str
    tracks: list[dict[str]]


@dataclass
class LastFMUserTopTracksProcessedInfo(InfoBase):
    """
    dataclass used to store information about lastfm user and their tracks (processed & ready for madness bracket)

    :attr username: (str) lastfm username
    :attr tracks: (list[TrackInfo]) list of user's top tracks (processed as TrackInfo objects)
    """
    username: str
    tracks: list[TrackInfo]


class LastFMPaginationInfo(NamedTuple):
    """
    namedtuple used to store information about pagination from lastfm

    :attr page: (int) current page
    :attr total_pages: (int) total amount of pages
    """
    page: int
    total_pages: int
