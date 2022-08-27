import json
import random

from madnessbracket import cache
from madnessbracket.music_apis.lastfm_api.lastfm_api import lastfm_get_response


@cache.memoize(timeout=36000)
def lastfm_get_user_top_tracks(username: str):
    """get user's top tracks on lastfm

    Args:
        username (str): user's nickname on Last.fm

    Returns:
        (list): of user's top tracks
    """
    print("GETTING LASTFM USER TOP TRACKS")
    MAX_PAGES = 3
    LIMIT = 50
    TIME_PERIODS = [
        "overall",
        "7day",
        "1month",
        "3month",
        "6month",
        "12month"
    ]
    time_period = random.choice(TIME_PERIODS)
    page = 1
    top_tracks = []
    for _ in range(MAX_PAGES):
        response = lastfm_get_response({
            'method': 'user.getTopTracks',
            'user': username,
            'period': time_period,
            'limit': LIMIT,
            'page': page
        })
        # in case of an error, return None
        if response.status_code != 200:
            print('lastfm response NOT OK')
            if page > 1:
                print("returning tracks, even though response's not OK (but page > 1)")
                return top_tracks
            return None, None
        page = int(response.json()['toptracks']['@attr']['page'])
        total_pages = min(
            int(response.json()['toptracks']['@attr']['totalPages']), MAX_PAGES)
        try:
            tracks = response.json()["toptracks"]["track"]
            top_tracks.extend(tracks)
        except (KeyError, TypeError, json.decoder.JSONDecodeError) as e:
            print(e)
            return None, None
        page += 1
        if page > total_pages:
            break
        if page > 1:
            continue
        try:
            correct_username = response.json()['toptracks']['@attr']['user']
            username = correct_username
        except (KeyError, ValueError) as e:
            print(e)
            pass
    print(f"LASTFM USER TOP TRACKS TOTAL: {len(top_tracks)}")
    return username, top_tracks
