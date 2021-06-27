from sqlalchemy.event import listen

from madnessbracket import cache, db
from madnessbracket.dev.lastfm.lastfm_artist_handlers import lastfm_get_artist_correct_name
from madnessbracket.dev.spotify.spotify_artist_handlers import get_spotify_artist_top_tracks
from madnessbracket.models import Artist, Song
from madnessbracket.musician.prepare_tracks import prepare_tracks_for_musician, process_tracks_from_spotify, \
    process_tracks_from_db
from madnessbracket.utilities.db_extensions import load_unicode_extension
from madnessbracket.utilities.logging_handlers import log_artist_missing_from_db


def get_musician_bracket_data(artist_name: str, bracket_limit: int):
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
    artist_tracks = prepare_tracks_for_musician(artist_tracks, bracket_limit)

    tracks = {
        "tracks": artist_tracks,
        "description": artist_tracks[0]["artist_name"].upper(),
        "value1": artist_tracks[0]["artist_name"],
        "extra": None
    }
    return tracks


def get_artists_tracks(artist_name: str, bracket_limit: int):
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
    # correct user's input via lastfm's api
    correct_name = lastfm_get_artist_correct_name(artist_name)
    # artist_name = artist_name.lower()
    print('corrected name:', artist_name, len(artist_name))
    # go through database first
    tracks = get_tracks_via_database(artist_name, correct_name)
    # if nothing found, go through a fallback function — via spotify
    if not tracks:
        artist_name = correct_name if correct_name else artist_name
        tracks = get_tracks_via_spotify(artist_name)
    if not tracks:
        print(f"nothing found at all for {artist_name}")
        return None
    return tracks


@cache.memoize(timeout=3600)
def get_tracks_via_database(artist_name: str, correct_name: str):
    """get artist's top tracks/songs via database

    Args:
        artist_name (str): artist's name
        correct_name (str): lastfm-corrected artist's name
    Returns:
        (list): a list of tracks from by a particular artist found in database
    """
    # set max song limit
    SONG_LIMIT = 100
    listen(db.engine, 'connect', load_unicode_extension)
    artist = Artist.query.filter(Artist.name.like(artist_name)).first()
    if not artist:
        # no such artist found
        if not correct_name:
            return None
        if correct_name.lower() == artist_name.lower():
            return None
        artist = Artist.query.filter(Artist.name.like(correct_name)).first()
        if not artist:
            print("no artist found on db")
            return None
    # find top tracks in descending order (most listened first)
    track_entries = Song.query.filter_by(artist=artist).order_by(
        Song.rating.desc()).limit(SONG_LIMIT).all()
    if not track_entries:
        return None
    print(track_entries, len(track_entries))
    print(list(set(track_entries)), len(set(track_entries)))
    processed_tracks = process_tracks_from_db(track_entries)
    return processed_tracks


@cache.memoize(timeout=3600)
def get_tracks_via_spotify(artist_name: str):
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
        spotify_artist_name = processed_tracks[0]["artist_name"]
        artist_name = spotify_artist_name
    except (IndexError, ValueError) as e:
        print(e)
    # log newly found artist
    if processed_tracks:
        log_artist_missing_from_db(artist_name)
    return processed_tracks
