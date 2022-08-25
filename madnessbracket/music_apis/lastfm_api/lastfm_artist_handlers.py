import json
from typing import Optional

from madnessbracket import cache
from madnessbracket.music_apis.lastfm_api.lastfm_api import lastfm_get_response


@cache.memoize(timeout=3600)
def lastfm_get_artist_correct_name(artist_name: str) -> Optional[str]:
    """
    Use the last.fm corrections data to check whether the supplied artist has a correction to a canonical artist
    :param artist_name: (str) artist's name as is
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
    return correct_name


def lastfm_get_artist_top_tracks(artist: str):
    """get artist's top tracks on lastfm (by scrobbles)

    Args:
        artist (str): artist's name

    Returns:
        (list): of artist's top tracks
    """
    response = lastfm_get_response({
        'method': 'artist.getTopTracks',
        'artist': artist,
        'limit': 32
    })
    # in case of an error, return None
    if response.status_code != 200:
        return None
    try:
        top_tracks = response.json(
        )["toptracks"]["track"]
    except (KeyError, TypeError, json.decoder.JSONDecodeError):
        return None
    print(len(top_tracks))
    return top_tracks