import os
import random
import json
from flask import current_app


def get_top_rated_songs():
    """
    picks random selection of songs considered best*
    * by Pitchfork, (Rolling Stones, …) # TODO: add RS500/NME
    """
    filename = 'extended_classics_list.json'
    filepath = os.path.join(current_app.root_path, 'charts', filename)
    try:
        with open(filepath, encoding='utf-8') as f:
            songs = json.load(f)
    except IOError as e:
        print('file not found', e)
        return None
    # shuffle the songs
    random.shuffle(songs)
    # init dict
    tracks = {
        "tracks": [],
        "description": "charts"
    }
    # iterate through tracks
    for song in songs:
        name = song['title']
        artist_name = song['artist_name']
        preview_url = song["preview_url"]
        album_colors = song["album_colors"]
        text_color = song["text_color"]

        a_track_info = {
            "artist_name": artist_name,
            "track_title": name,
            "spotify_preview_url": preview_url,
            "album_colors": album_colors,
            "text_color": text_color
            # TODO: add preview urls to the original json file
        }
        tracks["tracks"].append(a_track_info)
    return tracks
