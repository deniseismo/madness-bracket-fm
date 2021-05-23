import json

from madnessbracket.dev.lastfm.lastfm_api import lastfm_get_response


def lastfm_get_user_top_tracks(username: str):
    """get user's top tracks on lastfm

    Args:
        username (str): user's nickname on Last.fm

    Returns:
        (list): of user's top tracks
    """
    LIMIT = 50
    TIME_PERIODS = [
        "overall",
        "7day",
        "1month",
        "3month",
        "6month",
        "12month"
    ]
    response = lastfm_get_response({
        'method': 'user.getTopTracks',
        'user': username,
        'period': "overall",
        'limit': LIMIT
    })
    # in case of an error, return None
    if response.status_code != 200:
        return None
    try:
        top_tracks = response.json()["toptracks"]["track"]
    except (KeyError, TypeError, json.decoder.JSONDecodeError):
        return None
    print(len(top_tracks))
    return top_tracks
