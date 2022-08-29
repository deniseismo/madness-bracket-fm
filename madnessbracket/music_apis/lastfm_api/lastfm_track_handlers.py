import json
from typing import Optional

from madnessbracket.music_apis.lastfm_api.lastfm_api import lastfm_get_response


def lastfm_get_track_rating(track_title: str, artist_name: str) -> Optional[int]:
    """
    gets track's number of playcount as a metric of popularity
    :param track_title: track's title
    :param artist_name: artist's name
    """
    if not track_title or not artist_name:
        return None
    response = lastfm_get_response({
        'method': 'track.getInfo',
        'track': track_title,
        'artist': artist_name,
    })
    if response is None:
        return None
    # in case of an error, return None
    if response.status_code != 200:
        print(f"couldn't find {track_title} by {artist_name} on last.fm")
        return None
    try:
        track_playcount = response.json()['track']['playcount']
    except (KeyError, TypeError, json.JSONDecodeError) as e:
        print(e)
        return 0
    return int(track_playcount)
