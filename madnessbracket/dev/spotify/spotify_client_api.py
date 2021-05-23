import spotipy
import tekore as tk
from flask import current_app
from spotipy.oauth2 import SpotifyClientCredentials


def get_spotify_spotipy_client():
    """get a spotify client via spotipy library

    Returns:
        an instance of a Spotify client
    """
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
        client_id=current_app.config['SPOTIFY_CLIENT_ID'],
        client_secret=current_app.config['SPOTIFY_CLIENT_SECRET']
    ))
    return spotify


def get_spotify_tekore_client(asynchronous=False):
    """get a spotify client via tekore library

    Returns:
        an instance of a Spotify client
    """
    client_id = current_app.config['SPOTIFY_CLIENT_ID']
    client_secret = current_app.config['SPOTIFY_CLIENT_SECRET']

    app_token = tk.request_client_token(
        client_id=client_id, client_secret=client_secret)
    spotify_tekore_client = tk.Spotify(app_token, asynchronous=asynchronous)
    return spotify_tekore_client
