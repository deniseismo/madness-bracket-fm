import random
import tekore as tk
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from flask import current_app

from madnessbracket.utilities.track_processing import get_filtered_name


def get_spotify_spotipy_client():
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
        client_id=current_app.config['SPOTIFY_CLIENT_ID'],
        client_secret=current_app.config['SPOTIFY_CLIENT_SECRET']
    ))
    return spotify


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
    query = f"{artist_name}"
    artist_info, = spotify_tekore_client.search(
        query=query, types=('artist',), limit=50, market="SE")
    # in case of not getting any response
    if not artist_info:
        print("no info about the artist returned at all")
        return None
    # in case no items found
    if artist_info.total == 0:
        print(artist_info)
        print("no artists found")
        return None
    # iterate over artists found
    print(artist_info.total)
    for index, artist in enumerate(artist_info.items):
        print(index, artist.name)
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
    # artist_id = get_spotify_artist_id(artist_name, spotify_tekore_client) # get ID via tekore
    artist_id = spotipy_get_artist_id(artist_name)  # get ID via spotipy
    print("artist spotify id", artist_id)
    top_tracks = spotify_tekore_client.artist_top_tracks(artist_id, 'US')
    # in case of not getting any response
    if not top_tracks:
        return None
    return top_tracks


def spotipy_get_artist_id(artist_name: str):
    """
    search for an artist's id
    :param artist_name: artist's name
    :return: album_image_url
    """
    spotify = get_spotify_spotipy_client()
    try:
        artist_info = spotify.search(
            q=artist_name, type="artist", limit=5, market='SE')
    except spotipy.exceptions.SpotifyException:
        return None
    if not artist_info:
        return None
    artist_id = None
    print(artist_info['artists']['items'])
    for item in artist_info['artists']['items']:
        print(item['name'].lower(), artist_name.lower())
        if item['name'].lower() == artist_name.lower():
            try:
                print('artists name are equal!')
                artist_id = item['id']
                break
            except KeyError:
                return None
    return artist_id
