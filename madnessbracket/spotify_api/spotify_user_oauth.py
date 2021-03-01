import pickle
import random

import tekore as tk
from flask import Blueprint, current_app, session
from madnessbracket.models import User

spotify = Blueprint('spotify', __name__)

spotify_tekore_client = tk.Spotify()


def get_spotify_auth():
    """
    get a User auth object
    :return: redirect url
    """
    conf = (
        current_app.config['SPOTIFY_CLIENT_ID'],
        current_app.config['SPOTIFY_CLIENT_SECRET'],
        current_app.config['SPOTIFY_REDIRECT_URI']
    )
    cred = tk.Credentials(*conf)
    # scopes allow client to read user's name, id, avatar & user's top artists/tracks
    scope = tk.Scope(tk.scope.user_top_read, tk.scope.user_read_private)
    auth = tk.UserAuth(cred, scope)
    return auth


def check_spotify():
    """
    checks if the person's logged in the token's not expired
    refreshes token if present
    :return: (user, token)
    """
    user = session.get('user', None)
    token = session.get('token', None)
    if token:
        token = pickle.loads(session.get('token', None))

    if user is None or token is None:
        print('either user or token is None')
        session.pop('user', None)
        session.pop('token', None)
        return None, None

    if token.is_expiring:
        # get new access token
        print('token is expiring')
        conf = (
            current_app.config['SPOTIFY_CLIENT_ID'],
            current_app.config['SPOTIFY_CLIENT_SECRET'],
            current_app.config['SPOTIFY_REDIRECT_URI']
        )
        print(user)
        cred = tk.Credentials(*conf)
        user_entry = User.query.filter_by(spotify_id=user).first()
        if user_entry:
            print(f'user found: {user}')
            # get user's refresh token from db
            refresh_token = user_entry.spotify_token
            print(f'refresh_token: {refresh_token}')
            if refresh_token:
                # get new token via refresh token
                token = cred.refresh_user_token(refresh_token)
                session['token'] = pickle.dumps(token)

    return user, token


def get_spotify_user_info(token):
    """

    :param token: a Spotify access token
    :return: user info {username, user_image}
    """
    print('getting user info...')
    print(token)
    try:
        with spotify_tekore_client.token_as(token):
            print('getting here')
            current_user = spotify_tekore_client.current_user()
            username = current_user.display_name
            current_user_image_list = current_user.images
            country = current_user.country
            if current_user_image_list:
                try:
                    user_image = current_user.images[0].url
                except (KeyError, IndexError, TypeError):
                    user_image = None
            else:
                user_image = None

    except tk.HTTPError:
        return None
    user_info = {
        "username": username,
        "user_image": user_image,
        "country": country
    }
    return user_info


def spotify_get_users_top_tracks(token):
    """
    :param token: an access token
    :return: current user's top track items
    """
    # spotify's internal 'time spans': gives different selections of your fav. tracks based on time period
    time_periods = ['short_term', 'medium_term', 'long_term']
    if not token:
        return None
    try:
        with spotify_tekore_client.token_as(token):
            # get user's top 50 tracks (pick time span at random)
            top_tracks = spotify_tekore_client.current_user_top_tracks(
                limit=50, time_range=random.choice(time_periods))
    except tk.HTTPError:
        return None

    if not top_tracks:
        return None

    if not top_tracks.items:
        return None
    print(top_tracks.total)
    if len(top_tracks.items) < 4:
        print('not enought tracks')
        return None
    return top_tracks.items
