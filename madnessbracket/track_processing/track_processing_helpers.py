import random

from madnessbracket.schemas.response import TracksInfoResponse
from madnessbracket.schemas.track_schema import TrackInfo


def make_tracks_info_response(
        tracks: list[TrackInfo],
        description: str,
        value1: str = None,
        value2: str = None,
        extra: str = None
) -> TracksInfoResponse:
    """
        tracks = {
        "tracks": battle_tracks,
        "description": description,
        "value1": artist_1_name,
        "value2": artist_2_name,
        "extra": "artists_battle"
    }
    make a TracksInfoResponse (ready to be jsonified and sent to the user)
    :param tracks: a list of processed and ready TrackInfo
    :return: AlbumCoversResponse
    """
    tracks_info_response = TracksInfoResponse(
        tracks=tracks,
        description=description
    )
    if value1:
        tracks_info_response.value1 = value1
    if value2:
        tracks_info_response.value2 = value2
    if extra:
        tracks_info_response.extra = extra
    return tracks_info_response


def sort_artist_tracks(tracks: list[TrackInfo]) -> bool:
    """
    sort artist tracks randomly
    :param tracks: (list[TrackInfo])
    """
    random.seed()
    random.shuffle(tracks)
    return True
