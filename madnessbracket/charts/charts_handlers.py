import json
import os
import random

from flask import current_app

from madnessbracket import cache
from madnessbracket.charts.prepare_tracks import prepare_tracks_for_charts


def get_songs_considered_best(upper_limit: int):
    """
    picks random selection of songs considered best*
    * by Pitchfork, (Rolling Stones, …) # TODO: add RS500/NME
    """
    songs = load_best_songs_from_the_file()
    if not songs:
        return None
    # shuffle the songs
    random.shuffle(songs)
    processed_tracks = process_charts_songs(songs)
    tracks = {
        "tracks": processed_tracks,
        "description": "charts",
        "secret": None,
    }
    tracks = prepare_tracks_for_charts(tracks, upper_limit)
    return tracks


@cache.memoize(timeout=3600)
def load_best_songs_from_the_file():
    """load all the best (according to some papers) songs of all time

    Returns:
        [list]: of the best songs
    """
    filename = 'nme_top_500_extended.json'
    filepath = os.path.join(current_app.root_path, 'charts', filename)
    try:
        with open(filepath, encoding='utf-8') as f:
            songs = json.load(f)
    except IOError as e:
        print('file not found', e)
        return None
    return songs


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
