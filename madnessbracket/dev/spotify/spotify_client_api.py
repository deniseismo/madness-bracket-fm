import random
import tekore as tk
from flask import current_app

from madnessbracket.utilities.track_processing import get_filtered_name



def get_spotify_tekore_client():
    client_id = current_app.config['SPOTIFY_CLIENT_ID']
    client_secret = current_app.config['SPOTIFY_CLIENT_SECRET']

    app_token = tk.request_client_token(
        client_id=client_id, client_secret=client_secret)
    spotify_tekore_client = tk.Spotify(app_token)
    return spotify_tekore_client


def get_spotify_track_info(track_title: str, artist_name: str, tekore_client=None):
    """
    search for a track & get the track info
    :param track_title: track's title
    :param artist_name: artist's name
    """
    if not track_title or not artist_name:
        return None
    # if tekore client is not provided, get a new one
    if not tekore_client:
        spotify_tekore_client = get_spotify_tekore_client()
    else:
        spotify_tekore_client = tekore_client
    query = f"track:{track_title} artist:{artist_name}"
    tracks_info, = spotify_tekore_client.search(query=query, types=('track',))
    # in case of not getting any response
    if not tracks_info:
        return None
    # in case no items found
    if tracks_info.total == 0:
        return None
    return tracks_info.items[0]


def get_spotify_artist_id(artist_name: str, tekore_client=None):
    """
    get artist's spotify id
    """
    if not artist_name:
        return None
    # if tekore client is not provided, get a new one
    if not tekore_client:
        spotify_tekore_client = get_spotify_tekore_client()
    else:
        spotify_tekore_client = tekore_client
    spotify_tekore_client = get_spotify_tekore_client()
    query = f"artist: {artist_name}"
    artist_info, = spotify_tekore_client.search(query=query, types=('artist',))
    # in case of not getting any response
    if not artist_info:
        return None
    # in case no items found
    if artist_info.total == 0:
        return None
    # iterate over artists found
    for artist in artist_info.items:
        # find the right one
        if artist.name.lower() == artist_name.lower():
            return artist.id
    return None


def get_spotify_artist_top_tracks(artist_name: str, tekore_client=None):
    """
    get artist's top tracks according to spotify
    :param artist_name: spotify's artist id
    """
    if not artist_name:
        return None
    # if tekore client is not provided, get a new one
    if not tekore_client:
        spotify_tekore_client = get_spotify_tekore_client()
    else:
        spotify_tekore_client = tekore_client
    artist_id = get_spotify_artist_id(artist_name, spotify_tekore_client)
    top_tracks = spotify_tekore_client.artist_top_tracks(artist_id, 'RU')
    # in case of not getting any response
    if not top_tracks:
        return None
    return top_tracks
