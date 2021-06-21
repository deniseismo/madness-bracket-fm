import json
import random

from madnessbracket import cache
from madnessbracket.dev.lastfm.lastfm_api import lastfm_get_response


@cache.memoize(timeout=36000)
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
        'period': random.choice(TIME_PERIODS),
        'limit': LIMIT
    })
    # in case of an error, return None
    if response.status_code != 200:
        print('lastfm response NOT OK')
        return None
    try:
        top_tracks = response.json()["toptracks"]["track"]
    except (KeyError, TypeError, json.decoder.JSONDecodeError) as e:
        print(e)
        return None
    try:
        correct_username = response.json()['toptracks']['@attr']['user']
        username = correct_username
    except (KeyError, ValueError) as e:
        print(e)
        return None
    print(len(top_tracks))
    return username, top_tracks
