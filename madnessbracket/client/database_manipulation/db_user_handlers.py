from madnessbracket import db
from madnessbracket.models import User


def add_new_spotify_user_to_database(spotify_user_id: str, refresh_token: str) -> bool:
    """
    add new spotify user (spotify id, refresh token) to database
    :param spotify_user_id: user's id on Spotify
    :param refresh_token: refresh token for generating new access tokens
    """
    user_entry = User(spotify_id=spotify_user_id, spotify_token=refresh_token)
    db.session.add(user_entry)
    db.session.commit()
    return True
