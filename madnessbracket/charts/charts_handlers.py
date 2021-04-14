import os
import random
import json
from flask import current_app


def get_songs_considered_best():
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
    processed_tracks = process_charts_songs(songs)
    tracks = {
        "tracks": processed_tracks,
        "description": "charts"
    }
    return tracks


def process_charts_songs(tracks: list):
    """
    processes songs from charts creating a list of dicts with all the needed info about tracks
    :param tracks:
    :return: a list of dict with all the info about particular songs
    """
    # iterate through tracks
    processed_tracks = []
    for track in tracks:
        name = track['title']
        artist_name = track['artist_name']
        preview_url = track["preview_url"]
        album_colors = track["album_colors"]
        text_color = track["text_color"]

        a_track_info = {
            "artist_name": artist_name,
            "track_title": name,
            "spotify_preview_url": preview_url,
            "album_colors": album_colors,
            "text_color": text_color
        }
        processed_tracks.append(a_track_info)
    return processed_tracks
