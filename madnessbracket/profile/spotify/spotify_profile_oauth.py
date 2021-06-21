import pickle

import tekore as tk
from flask import Blueprint, current_app, session

from madnessbracket.models import User

spotify = Blueprint('spotify', __name__)

spotify_tekore_client = tk.Spotify()


def get_spotify_auth():
    """get a User auth object
    Returns:
        auth
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


def check_spotify_login():
    """checks if the person's logged in the token's not expired
    refreshes token if present

    Returns:
        (user, token)
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
        print(f"user entry: {user_entry}")
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
    """a Spotify access token
    :return: user info {username, user_image}

    Args:
        token: token

    Returns:
        user info {username, user_image}
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
            print(f"current user: {current_user}")
            if current_user_image_list:
                try:
                    user_image = current_user.images[0].url
                except (KeyError, IndexError, TypeError):
                    user_image = None
            else:
                user_image = None

    except tk.HTTPError as e:
        print(e)
        return None
    user_info = {
        "username": username,
        "user_image": user_image,
        "country": country
    }
    print(f"user info: {user_info}")
    return user_info
