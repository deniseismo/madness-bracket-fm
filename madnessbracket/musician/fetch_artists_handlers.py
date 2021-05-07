import json
import os

from flask import current_app

from madnessbracket import cache


@cache.memoize(timeout=36000)
def get_filtered_artists_suggestions(query):
    """get appropriate artists suggestions according to the given search input (query)

    Args:
        query (str): user's input
    """
    try:
        filename = "all_artists.json"
        filepath = os.path.join(current_app.root_path, "musician", filename)
        with open(filepath, encoding="UTF-8") as file:
            artists_list = json.load(file)
    except (IOError, OSError) as e:
        print(e)
        return []
    print(query)
    filtered_artists_list = []
    # check if the input's not empty
    if query and artists_list:
        for artist in artists_list:
            if query in artist.lower():
                filtered_artists_list.append(artist)
    return filtered_artists_list
