from typing import Optional

from madnessbracket.schemas.characteristics import TrackIdentity
from madnessbracket.schemas.track_schema import TrackInfo
from madnessbracket.utilities.name_filtering import get_filtered_name


def process_tracks_from_lastfm(tracks: list[dict[str]]) -> list[TrackInfo]:
    """
    process/parse a list of dicts we got from last.fm into TrackInfo objects with all the info
    :param tracks:
    :return:
    """
    processed_tracks = []
    track_ids = set()
    for track_entry in tracks:
        track_info = process_a_track_from_lastfm(track_entry, track_ids)
        if not track_info:
            continue
        processed_tracks.append(track_info)
    return processed_tracks


def process_a_track_from_lastfm(track_entry: dict[str], track_ids: set) -> Optional[TrackInfo]:
    """
    process track info (dict) from last.fm
    :param track_entry: (dict[str]) track information from last.fm
    :param track_ids: (set) a set of TrackIdentity tuples used for filtering out duplicate songs
    :return: (TrackInfo)
    """
    try:
        artist_name = track_entry['artist']['name']
        track_title = track_entry['name']
    except (KeyError, TypeError) as e:
        print("error when parsing lastfm tracks", e)
        return None
    filtered_title = get_filtered_name(track_title)
    track_id = TrackIdentity(title=filtered_title, artist_name=artist_name)
    if track_id in track_ids:
        print(f"--{track_id=} is already in track_ids")
        return None
    track_ids.add(track_id)
    track_info = TrackInfo(
        track_title=filtered_title,
        artist_name=artist_name
    )
    return track_info
