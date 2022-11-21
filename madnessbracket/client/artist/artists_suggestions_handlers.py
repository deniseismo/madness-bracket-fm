import json
import os
from typing import Optional

from flask import current_app

from madnessbracket import cache


@cache.memoize(timeout=60000)
def _load_all_artists():
    """
    load a list of artists from disk
    :return:
    """
    ARTISTS_LIST_FILENAME = "all_artists.json"
    ARTISTS_LIST_PATH = os.path.join(current_app.root_path, "client", "artist", ARTISTS_LIST_FILENAME)
    try:
        with open(ARTISTS_LIST_PATH) as jsonfile:
            music_genres_list = json.load(jsonfile)
    except (IOError, OSError) as e:
        print(e)
        return []
    return music_genres_list


@cache.memoize(timeout=36000)
def get_filtered_artists_suggestions(query: Optional[str]) -> list[str]:
    """get appropriate artists suggestions according to the given search input (query)

    Args:
        query (str): user's input
    """
    artists_list = _load_all_artists()
    print(query)
    filtered_artists_list = []
    # check if the input's not empty
    if query and artists_list:
        for artist in artists_list:
            if query in artist.lower():
                filtered_artists_list.append(artist)
    return filtered_artists_list
