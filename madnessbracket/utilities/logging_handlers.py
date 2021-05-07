import csv
import os

from flask import current_app


def log_missing_info(info):
    """
    logs missing info (missing songs/albums/releases, etc.) to a file
    """
    filename = 'missing_info.csv'
    filepath = os.path.join(current_app.root_path, 'dev/logs', filename)
    try:
        with open(filepath, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([info])
    except IOError as e:
        print('file not found', e)
        return None


def log_new_songs(new_song_info):
    """
    log newly added songs
    """
    filename = 'new_songs_from_top_artists_charts.csv'
    filepath = os.path.join(current_app.root_path, 'dev/logs', filename)
    try:
        with open(filepath, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([new_song_info])
    except IOError as e:
        print('file not found', e)
        return None


def log_arbitrary_data(data_to_log: str, filename: str):
    """
    :param data_to_log: any data you want to log in
    :param filename: filename to save data into
    :return:
    """
    filepath = os.path.join(current_app.root_path, 'dev/logs', filename)
    try:
        with open(filepath, 'a+', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([data_to_log])
    except IOError as e:
        print('file not found', e)
        return None


def log_artist_missing_from_db(artist_name: str):
    """
    log newly found artist that's been missing from database
    :param artist_name: artist's name
    """
    filename = 'artists_missing_from_db.csv'
    filepath = os.path.join(current_app.root_path, 'dev/logs', filename)
    try:
        with open(filepath, 'r', newline='', encoding='utf-8') as file:
            contents = file.read()
    except (IOError, OSError):
        return False
    if artist_name in contents:
        print(f"{artist_name}'s already been added to the list")
        # no need to add the artist
        return False
    log_arbitrary_data(artist_name, filename)


def log_winner_track(artist_name: str, track_title: str, bracket_type: str, description: str):
    filename = 'winner_tracks.csv'
    filepath = os.path.join(current_app.root_path, 'dev/logs', filename)
    fieldnames = ["artist_name", "track_title", "bracket_type", "description"]
    try:
        with open(filepath, "a+", encoding="utf-8") as file:
            csvfile = csv.DictWriter(file, fieldnames=fieldnames)
            winner_track_data = {
                "artist_name": artist_name,
                "track_title": track_title,
                "bracket_type": bracket_type,
                "description": description
            }
            csvfile.writerow(winner_track_data)
    except (IOError, OSError):
        print(f"couldn't open file: {filename}")
        return False
