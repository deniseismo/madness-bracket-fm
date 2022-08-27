from typing import Optional

from madnessbracket import cache
from madnessbracket.client.database_manipulation.db_artist_handlers import db_get_artist
from madnessbracket.client.database_manipulation.db_track_handlers import db_get_tracks_by_artist_entry
from madnessbracket.client.artist.prepare_tracks import prepare_tracks_for_musician
from madnessbracket.music_apis.lastfm_api.lastfm_artist_handlers import lastfm_get_artist_correct_name
from madnessbracket.music_apis.spotify_api.spotify_artist_handlers import get_spotify_artist_top_tracks
from madnessbracket.schemas.track_schema import TrackInfo
from madnessbracket.track_processing.process_tracks_from_database import process_tracks_from_db
from madnessbracket.track_processing.process_tracks_from_spotify import process_tracks_from_spotify
from madnessbracket.utilities.logging_handlers import log_artist_missing_from_db


def get_musician_bracket_data(artist_name: str, bracket_limit: int) -> Optional[dict]:
    """
    a shortcut function that combines all the other musician handlers
    :param artist_name: artist's name
    :param bracket_limit: chosen bracket upper limit
    :return: a dict with all the musician bracket data
    """
    if not artist_name or not bracket_limit:
        # no artist provided or bracket limit provided
        return None
    artist_correct_name = lastfm_get_artist_correct_name(artist_name)
    if artist_correct_name:
        artist_name = artist_correct_name
    artist_tracks = get_artists_tracks(artist_name, bracket_limit)
    if not artist_tracks:
        return None
    artist_tracks = prepare_tracks_for_musician(artist_tracks, bracket_limit)

    tracks = {
        "tracks": artist_tracks,
        "description": artist_tracks[0]["artist_name"].upper(),
        "value1": artist_tracks[0]["artist_name"],
        "extra": None
    }
    return tracks


def get_artists_tracks(artist_name: str, bracket_limit: int) -> Optional[list[TrackInfo]]:
    """gets top tracks by a particular artist
    first it goes through database,
    if nothing found, goes through spotify fallback function

    Args:
        artist_name (str): artist's name
        bracket_limit: chosen bracket upper limit
    Returns:
        [dict]: a dict with a list of 'track info' dicts

    """
    if not artist_name or not bracket_limit:
        # no artist provided
        return None
    # go through database first
    tracks = get_artist_tracks_from_database(artist_name)
    # if nothing found, go through a fallback function — via spotify
    if not tracks:
        tracks = get_tracks_via_spotify(artist_name)
    if not tracks:
        print(f"nothing found at all for {artist_name}")
        return None
    return tracks


@cache.memoize(timeout=3600)
def get_artist_tracks_from_database(artist_name: str) -> Optional[list[TrackInfo]]:
    """
    get artist's top track from database (sorted by rating (popularity/number of scrobbles)
    :param artist_name: (str) artist's name
    :return: (list[TrackInfo]) a list of processed TrackInfo with all the information about tracks from db
    """
    artist_entry = db_get_artist(artist_name)
    if not artist_entry:
        return None
    # find top tracks in descending order (most listened first)
    track_entries = db_get_tracks_by_artist_entry(artist_entry)
    if not track_entries:
        return None
    processed_tracks = process_tracks_from_db(track_entries)
    return processed_tracks


@cache.memoize(timeout=3600)
def get_tracks_via_spotify(artist_name: str) -> Optional[list[TrackInfo]]:
    """a fallback function for getting top tracks if artist's missing from db

    Args:
        artist_name (str): artist's name

    Returns:
        (list): a list of tracks by a particular artist found on spotify
    """
    print(f"trying to get {artist_name} via Spotify")
    track_entries = get_spotify_artist_top_tracks(artist_name)
    if not track_entries:
        print(f"could NOT find {artist_name} via Spotify")
        return None
    print(track_entries)
    processed_tracks = process_tracks_from_spotify(track_entries)
    try:
        spotify_artist_name = processed_tracks[0].artist_name
        artist_name = spotify_artist_name
    except (IndexError, ValueError) as e:
        print(e)
    # log newly found artist
    if processed_tracks:
        log_artist_missing_from_db(artist_name)
    return processed_tracks
