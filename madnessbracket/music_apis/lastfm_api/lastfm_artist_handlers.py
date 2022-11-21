import json
import time
from typing import Optional

from madnessbracket.music_apis.lastfm_api.lastfm_api import lastfm_get_response


def lastfm_get_artist_correct_name(artist_name: str, delay: bool = False) -> Optional[str]:
    """
    Use the last.fm corrections data to check whether the supplied artist has a correction to a canonical artist
    :param artist_name: (str) artist's name as is
    :param delay: (bool) delay request so as not to get banned
    :return: corrected version of the artist's name
    """
    response = lastfm_get_response({
        'method': 'artist.getCorrection',
        'artist': artist_name
    })
    if not response:
        return None
    # in case of an error, return None
    if response.status_code != 200:
        return None
    try:
        correct_name = response.json()["corrections"]["correction"]["artist"]["name"]
    except (KeyError, TypeError, json.decoder.JSONDecodeError) as e:
        print(e)
        return None
    if delay:
        if not getattr(response, 'from_cache', False):
            time.sleep(0.6)
    return correct_name
