import requests_cache
import requests
import random
import json
import os
import sys


from flask import current_app
# from madnessbracket import create_app
# app = create_app()
# app.app_context().push()


requests_cache.install_cache()


def lastfm_get_response(payload: dict):
    """
    get response
    :param: payload: a dict with all the info on a particular request
    """
    # define headers and URL
    headers = {'user-agent': current_app.config['LASTFM_USER_AGENT']}
    url = 'http://ws.audioscrobbler.com/2.0/'
    # Add API key and format to the payload
    payload['api_key'] = current_app.config['LASTFM_API_KEY']
    payload['format'] = 'json'
    response = requests.get(url, headers=headers, params=payload)
    return response


def lastfm_get_track_rating(track_title, artist_name: str):
    """
    gets track's number of playcount as a metric of popularity
    :param track_title: track's title
    :param artist_name: artist's name
    """
    if not track_title or not artist_name:
        return None
    response = lastfm_get_response({
        'method': ' track.getInfo',
        'track': track_title,
        'artist': artist_name,
    })
    # in case of an error, return None
    if response.status_code != 200:
        print(f"couldn't find {track_title} by {artist} on last.fm")
        return None
    try:
        track_playcount = response.json()['track']['playcount']

    except (KeyError, IndexError, TypeError, ValueError) as e:
        print(e)
        print(f"no one seemed to listen for {track_title}")
        return 0
    return int(track_playcount)


def lastfm_get_artist_correct_name(artist: str):
    """
    Use the last.fm corrections data to check whether the supplied artist has a correction to a canonical artist
    :param artist: artist's name as is
    :return: corrected version of the artist's name
    """
    response = lastfm_get_response({
        'method': 'artist.getCorrection',
        'artist': artist
    })
    # in case of an error, return None
    if response.status_code != 200:
        return None
    try:
        correct_name = response.json(
        )["corrections"]["correction"]["artist"]["name"]
    except (KeyError, TypeError, json.decoder.JSONDecodeError):
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
