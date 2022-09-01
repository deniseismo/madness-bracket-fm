from typing import Optional

import spotipy
import tekore as tk
from flask import current_app
from spotipy.oauth2 import SpotifyClientCredentials
from tekore import ServiceUnavailable

from madnessbracket.utilities.helpers import timeit


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


@timeit
def get_spotify_tekore_client(asynchronous: bool = False) -> Optional[tk.Spotify]:
    """
    get spotify tekore library client
    :param asynchronous: async type of client
    :return: (tk.Spotify) Spotify tekore client
    """
    client_id = current_app.config['SPOTIFY_CLIENT_ID']
    client_secret = current_app.config['SPOTIFY_CLIENT_SECRET']
    try:
        app_token = tk.request_client_token(
            client_id=client_id, client_secret=client_secret)
        spotify_tekore_client = tk.Spotify(app_token, asynchronous=asynchronous)
    except ServiceUnavailable as e:
        print("can't get spotify tekore client")
        print(e)
        return None
    return spotify_tekore_client
