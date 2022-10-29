import pickle
import random
from typing import Optional

import tekore as tk
from flask import current_app, session
from tekore import Token, BadRequest

from madnessbracket.client.database_manipulation.db_user_handlers import delete_spotify_user_from_database
from madnessbracket.models import User
from madnessbracket.music_apis.spotify_api.spotify_client_api import get_spotify_tekore_client
from madnessbracket.schemas.spotify_user_info import SpotifyUserAuth, SpotifyUserProfile, SpotifyTopTracksInfo, \
    SpotifyTopTracksProcessedInfo
from madnessbracket.track_processing.process_tracks_from_spotify import process_tracks_from_spotify


def get_spotify_auth() -> tk.UserAuth:
    """
    get a tekore spotify User auth object
    :return: (tk.UserAuth)
    """
    conf = _get_app_spotify_credentials()
    cred = tk.Credentials(*conf)
    # scopes allow client to read user's name, id, avatar & user's top artists/tracks
    scope = tk.Scope(tk.scope.user_top_read, tk.scope.user_read_private)
    auth = tk.UserAuth(cred, scope)
    return auth


def _get_app_spotify_credentials() -> tuple[str, str, str]:
    """
    get spotify client credentials [client id, client secret, redirect uri]
    :return: (tuple[str, str, str]) spotify credentials [client id, client secret, redirect uri]
    """
    return (
        current_app.config['SPOTIFY_CLIENT_ID'],
        current_app.config['SPOTIFY_CLIENT_SECRET'],
        current_app.config['SPOTIFY_REDIRECT_URI']
    )


def authenticate_spotify_user() -> Optional[SpotifyUserAuth]:
    """
    checks/authenticates spotify user; refreshes token if present
    :return: (SpotifyUserAuth) with spotify user id and access token
    """
    user = session.get('user', None)
    token = session.get('token', None)
    if token:
        token = pickle.loads(session.get('token', None))

    if not (user and token):
        session.pop('user', None)
        session.pop('token', None)
        return SpotifyUserAuth(None, None)

    if token.is_expiring:
        try:
            token = _refresh_expiring_token(user)
        except BadRequest as e:
            # BadRequest might mean revoked and/or invalid token → clear user/token from session, delete user from db
            session.pop('user', None)
            session.pop('token', None)
            delete_spotify_user_from_database(user)
            return SpotifyUserAuth(None, None)

    return SpotifyUserAuth(user, token)


def _refresh_expiring_token(spotify_user_id: str) -> Optional[Token]:
    conf = _get_app_spotify_credentials()
    cred = tk.Credentials(*conf)
    user_entry = User.query.filter_by(spotify_id=spotify_user_id).first()
    if not user_entry:
        return None
    # get user's refresh token from db
    refresh_token = user_entry.spotify_token
    if not refresh_token:
        return None
    # get new token via refresh token
    token = cred.refresh_user_token(refresh_token)
    session['token'] = pickle.dumps(token)
    return token

def get_spotify_user_info(token) -> Optional[SpotifyUserProfile]:
    """
    get information about the current spotify user
    :param token: a Spotify access token
    :return: (SpotifyUserProfile) with spotify user info (username, avatar, country)
    """
    spotify_tekore_client = get_spotify_tekore_client()
    if not spotify_tekore_client:
        return None
    try:
        with spotify_tekore_client.token_as(token):
            current_user = spotify_tekore_client.current_user()

            username = current_user.display_name
            country = current_user.country
            user_image = None
            current_user_image_list = current_user.images
            if current_user_image_list:
                try:
                    user_image = current_user.images[0].url
                except (IndexError, TypeError) as e:
                    print(e)
    except tk.HTTPError:
        return None
    return SpotifyUserProfile(username=username, user_image=user_image, country=country)


def spotify_get_users_top_tracks(token) -> Optional[SpotifyTopTracksProcessedInfo]:
    """
    get all the best spotify user's tracks for a randomly chosen time period
    :param token: spotify user access token
    :return: (SpotifyTopTracksProcessedInfo) with username & all the tracks processed
    """
    if not token:
        return None
    # spotify's internal 'time spans': gives different selections of your fav. tracks based on time period
    time_ranges = ['short_term', 'medium_term', 'long_term']
    time_range = random.choice(time_ranges)
    spotify_top_tracks_info = _spotify_get_top_tracks_for_specific_time_range(token, time_range)
    if not spotify_top_tracks_info:
        return None
    username, spotify_user_top_tracks = spotify_top_tracks_info
    processed_tracks = process_tracks_from_spotify(spotify_user_top_tracks)
    return SpotifyTopTracksProcessedInfo(username=username, tracks=processed_tracks)


def _spotify_get_top_tracks_for_specific_time_range(token, time_range: str) -> Optional[SpotifyTopTracksInfo]:
    """
    get spotify user's best tracks for a specific time period (short term, medium term, long term)
    :param token: spotify user access token
    :param time_range: (str) one of the spotify's internal time spans: (['short_term', 'medium_term', 'long_term'])
    :return: (SpotifyTopTracksInfo) with username & FullTrack tracks (unprocessed spotify tekore track objects)
    """
    spotify_tekore_client = get_spotify_tekore_client()
    if not spotify_tekore_client:
        return None
    try:
        with spotify_tekore_client.token_as(token):
            current_user = spotify_tekore_client.current_user()
            username = current_user.display_name
            # get user's top 50 tracks (pick time span at random)
            top_tracks = spotify_tekore_client.current_user_top_tracks(
                limit=50,
                time_range=time_range
            )
    except tk.HTTPError:
        return None

    if not top_tracks:
        return None

    if not top_tracks.items:
        return None
    if len(top_tracks.items) < 4:
        print('not enough tracks')
        return None
    return SpotifyTopTracksInfo(username=username, tracks=top_tracks.items)
