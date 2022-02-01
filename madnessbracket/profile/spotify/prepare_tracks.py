import random
from typing import Optional

from madnessbracket.musician.prepare_tracks import process_tracks_from_spotify
from madnessbracket.utilities.bracket_sizing import get_capped_bracket_size


def prepare_spotify_tracks(track_items, bracket_limit) -> list:
    """
    prepare (cap & randomize) Spotify tracks
    :param track_items: Spotify (tekore lib) track items with full track info
    :param bracket_limit: upper bracket limit
    :return: processed tracks
    """
    number_of_tracks = len(track_items)
    tracks_cap = get_capped_bracket_size(number_of_tracks, bracket_limit)
    random.shuffle(track_items)
    capped_tracks = track_items[:tracks_cap]
    processed_tracks = process_tracks_from_spotify(capped_tracks)
    return processed_tracks


def process_spotify_tracks(track_items) -> Optional[dict]:
    """process spotify's track items
    :return: a fully prepared dict with all the tracks

    Args:
        track_items: track items from spotify (a list-like object from tekore library)

    Returns:
        (dict): a dict with tracks info
    """
    if not track_items:
        return None
    # initialize a dict to avoid KeyErrors
    tracks = {
        "tracks": []
    }
    # iterate through tracks
    for track in track_items:
        name = track.name
        artist_name = track.artists[0].name
        track_id = track.id
        preview_url = track.preview_url
        a_track_info = {
            "artist_name": artist_name,
            "track_title": name,
            "track_id": track_id,
            "preview_url": preview_url
        }
        tracks["tracks"].append(a_track_info)
    return tracks
