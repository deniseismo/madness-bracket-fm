from typing import Optional

from madnessbracket import cache
from madnessbracket.track_processing.track_preparation import prepare_tracks_for_artist
from madnessbracket.client.database_manipulation.db_artist_handlers import db_get_artist
from madnessbracket.client.database_manipulation.db_track_handlers import db_get_tracks_by_artist_entry
from madnessbracket.music_apis.spotify_api.spotify_artist_handlers import get_spotify_artist_top_tracks
from madnessbracket.schemas.track_schema import TrackInfo
from madnessbracket.track_processing.process_tracks_from_database import process_tracks_from_db
from madnessbracket.track_processing.process_tracks_from_spotify import process_tracks_from_spotify
from madnessbracket.utilities.logging_handlers import log_artist_missing_from_db


def get_tracks_for_artist(artist_name: str, bracket_limit: int) -> Optional[list[TrackInfo]]:
    """
    a shortcut function that combines all the other musician handlers
    :param artist_name: artist's name
    :param bracket_limit: chosen bracket upper limit
    :return: a dict with all the musician bracket data
    """
    if not artist_name or not bracket_limit:
        # no artist provided or bracket limit provided
        return None
    artist_tracks = get_artists_tracks(artist_name, bracket_limit)
    if not artist_tracks:
        return None
    artist_tracks = prepare_tracks_for_artist(artist_tracks, bracket_limit)
    return artist_tracks


def get_artists_tracks(artist_name: str, bracket_limit: int, max_songs_range: int = 100) -> Optional[list[TrackInfo]]:
    """
    find artist's tracks by artist's name (database, spotify)
    :param artist_name: (str) artist's name
    :param bracket_limit: (int) chosen bracket upper limit
    :param max_songs_range: (int) maximum number of top songs to choose from, defaults to top 100
    :return:
    """
    if not artist_name or not bracket_limit:
        # no artist provided
        return None
    # go through database first
    tracks = get_artist_tracks_from_database(artist_name, max_songs_range)
    # if nothing found, go through a fallback function — via spotify
    if not tracks:
        tracks = get_tracks_via_spotify(artist_name)
    if not tracks:
        print(f"nothing found at all for {artist_name}")
        return None
    return tracks


@cache.memoize(timeout=3600)
def get_artist_tracks_from_database(artist_name: str, max_songs_range: int = 100) -> Optional[list[TrackInfo]]:
    """
    get artist's top track from database (sorted by rating (popularity/number of scrobbles)
    :param artist_name: (str) artist's name
    :param max_songs_range: (int) maximum number of top songs to choose from, defaults to top 100
    :return: (list[TrackInfo]) a list of processed TrackInfo with all the information about tracks from db
    """
    artist_entry = db_get_artist(artist_name)
    if not artist_entry:
        return None
    # find top tracks in descending order (most listened first)
    track_entries = db_get_tracks_by_artist_entry(artist_entry, max_songs_range)
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
