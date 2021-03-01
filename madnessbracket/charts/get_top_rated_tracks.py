import os
import random
import json
from flask import current_app

def get_top_rated_songs():
    """
    picks random selection of songs considered best*
    * by Pitchfork, (Rolling Stones, …) # TODO: add RS500/NME
    """
    filename = os.path.join(current_app.root_path, 'charts\songs_considered_best.json')
    try:
        with open(filename, encoding='utf-8') as f:
            songs = json.load(f)
    except IOError as e:
        print('file not found', e)
        return None
    # shuffle the songs
    random.shuffle(songs)
    # init dict
    tracks = {
        "tracks": []
    }
    # iterate through tracks
    for song in songs:
        name = song['title']
        artist_name = song['artist']
        a_track_info = {
            "artist_name": artist_name,
            "track_title": name
            # TODO: add preview urls to the original json file
        }
        tracks["tracks"].append(a_track_info)
    return tracks
