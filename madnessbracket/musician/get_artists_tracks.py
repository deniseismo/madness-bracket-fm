from madnessbracket.models import Artist, Song
from madnessbracket.dev.lastfm.lastfm_api import lastfm_get_artist_correct_name
from madnessbracket.dev.spotify.spotify_client_api import get_spotify_artist_top_tracks
from sqlalchemy import func


def get_artists_tracks(artist_name: str):
    """
    :param artist_name: artist's name
    :return: a dict with a list of 'track info' dicts
    """
    if not artist_name:
        # no artist provided
        return None
    # correct user's input via lastfm's api
    correct_name = lastfm_get_artist_correct_name(artist_name)
    artist_name = correct_name if correct_name else artist_name
    artist_name = artist_name.lower()

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
    """
    get artist's top tracks/songs via database
    :param: artist_name: artist's name
    :return: return a dict with a list of 'track info' dicts
    """
    # set max song limit
    SONG_LIMIT = 50
    # artist = Artist.query.filter_by(name=artist_name).first()
    # find artist in the database
    artist = Artist.query.filter(func.lower(
        Artist.name) == artist_name).first()
    if not artist:
        # no such artist found
        return None
    # find top tracks in descending order (most listened first)
    track_entries = Song.query.filter_by(artist=artist).order_by(
        Song.rating.desc()).limit(SONG_LIMIT).all()
    if not track_entries:
        return None
    tracks = {
        "tracks": []
    }
    for track_entry in track_entries:
        track = {
            "track_title": track_entry.title,
            "artist_name": track_entry.artist.name,
            "spotify_preview_url": track_entry.spotify_preview_url if track_entry.spotify_preview_url else None,
            "album_colors": track_entry.album.album_cover_color.split(",")
        }
        tracks["tracks"].append(track)
    return tracks


def get_tracks_via_spotify(artist_name: str):
    """
    a fallback function for getting top tracks if artist's missing from db
    :param: artist_name: artist's name
    :return: return a dict with a list of 'track info' dicts
    """
    print(f"trying to get {artist_name} via Spotify")
    track_entries = get_spotify_artist_top_tracks(artist_name)
    if not track_entries:
        print(f"could NOT find {artist_name} via Spotify")
        return None
    tracks = {
        "tracks": []
    }
    for track_entry in track_entries:
        track = {
            "track_title": track_entry.name,
            "artist_name": track_entry.artist.name,
            "spotify_preview_url": track_entry.preview_url if track_entry.preview_url else None,
            "album_colors": None
        }
        tracks["tracks"].append(track)
    return tracks
