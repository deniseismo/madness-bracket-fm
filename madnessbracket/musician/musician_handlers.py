from madnessbracket.models import Artist, Song
from madnessbracket.dev.lastfm.lastfm_api import lastfm_get_artist_correct_name
from madnessbracket.dev.spotify.spotify_client_api import get_spotify_artist_top_tracks
from madnessbracket.dev.db_mgmt.color_mgmt.dominant_colors import get_file_from_url, get_image_dominant_colors
from madnessbracket.utilities.color_processing import get_contrast_color_for_two_color_gradient
from madnessbracket.utilities.logging_handlers import log_artist_missing_from_db


def get_artists_tracks(artist_name: str):
    """gets top tracks by a particular artist
    first it goes through database,
    if nothing found, goes through spotify fallback function

    Args:
        artist_name (str): artist's name

    Returns:
        [dict]: a dict with a list of 'track info' dicts
    """
    if not artist_name:
        # no artist provided
        return None
    # correct user's input via lastfm's api
    correct_name = lastfm_get_artist_correct_name(artist_name)
    artist_name = correct_name if correct_name else artist_name
    # artist_name = artist_name.lower()
    print('corrected name:', artist_name, len(artist_name))
    # go through database first
    tracks = get_tracks_via_database(artist_name)
    # if nothing found, go through a fallback function — via spotify
    if not tracks:
        tracks = get_tracks_via_spotify(artist_name)
    if not tracks:
        print(f"nothing found at all for {artist_name}")
        return None
    return tracks


def get_tracks_via_database(artist_name: str):
    """get artist's top tracks/songs via database

    Args:
        artist_name (str): artist's name

    Returns:
        (dict): a dict with a list of 'track info' dicts
    """
    # set max song limit
    SONG_LIMIT = 100
    artist = Artist.query.filter_by(name=artist_name).first()
    # find artist in the database
    # artist = Artist.query.filter(func.lower(
    #     Artist.name) == artist_name).first()
    if not artist:
        # no such artist found
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
    tracks = {
        "tracks": processed_tracks,
        "description": artist_name
    }
    return tracks


def get_tracks_via_spotify(artist_name: str):
    """a fallback function for getting top tracks if artist's missing from db

    Args:
        artist_name (str): artist's name

    Returns:
        (dict): a dict with a list of 'track info' dicts
    """
    print(f"trying to get {artist_name} via Spotify")
    track_entries = get_spotify_artist_top_tracks(artist_name)
    if not track_entries:
        print(f"could NOT find {artist_name} via Spotify")
        return None
    print(track_entries)
    processed_tracks = process_tracks_from_spotify(track_entries)
    tracks = {
        "tracks": processed_tracks,
        "description": artist_name
    }
    # log newly found artist
    if processed_tracks:
        log_artist_missing_from_db(artist_name)
    return tracks


def process_tracks_from_db(tracks: list):
    processed_tracks = []
    for track_entry in tracks:
        try:
            album_colors = track_entry.album.album_cover_color.split(",")
            dominant_color = album_colors[0]
            secondary_color = album_colors[1]
            text_color = get_contrast_color_for_two_color_gradient(
                dominant_color, secondary_color)
        except (AttributeError, NameError, TypeError, IndexError) as e:
            print(e)
            album_colors = None
            text_color = "white"
        track = {
            "track_title": track_entry.title,
            "artist_name": track_entry.artist.name,
            "spotify_preview_url": track_entry.spotify_preview_url if track_entry.spotify_preview_url else None,
            "album_colors": album_colors,
            "text_color": text_color
        }
        processed_tracks.append(track)
    return processed_tracks


def process_tracks_from_spotify(tracks: list):
    processed_tracks = []
    for track_entry in tracks:
        try:
            album_image_url = track_entry.album.images[-1].url
            image_file = get_file_from_url(album_image_url)
            album_colors = get_image_dominant_colors(
                image_file)
        except (IndexError, ValueError) as e:
            print(e)
            album_colors = None
        track = {
            "track_title": track_entry.name,
            "artist_name": track_entry.artists[0].name,
            "spotify_preview_url": track_entry.preview_url if track_entry.preview_url else None,
            "album_colors": album_colors
        }
        processed_tracks.append(track)
    return processed_tracks
