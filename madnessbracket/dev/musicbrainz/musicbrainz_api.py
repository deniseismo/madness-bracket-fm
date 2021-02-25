import random
import time
from datetime import datetime
import json
import musicbrainzngs
import requests
import requests_cache
from flask import current_app
from madnessbracket import create_app
from madnessbracket.dev.lastfm.lastfm_api import lastfm_get_track_rating

app = create_app()
app.app_context().push()


requests_cache.install_cache()

musicbrainzngs.set_useragent(
    *current_app.config['MUSIC_BRAINZ_USER_AGENT'].split(','))


def music_brainz_get_release_id_via_release_group(release_group_id: str):
    """
    get release id from a release_group id
    :param release_group_id: release group id from Music Brainz
    :return: realease id
    """
    release_group_info = musicbrainzngs.get_release_group_by_id(
        release_group_id, includes=['releases'])
    try:
        release_id = release_group_info['release-group']['release-list'][0]['id']
    except (IndexError, KeyError, TypeError, ValueError):
        print(f"couldn't find release id for {release_group_id}")
        return None
    print(release_id)
    return release_id



def music_brainz_get_release_tracklist(release_id: str):
    """
    get release group info by it id
    :param release_group_id: release group id from Music Brainz
    :return: info
    """
    release_info = musicbrainzngs.get_release_by_id(release_id, includes=['media', 'recordings'])
    if not release_info:
        print(f'no release info returned for {release_id}')
        return None
    try:
        tracklist = release_info['release']['medium-list'][0]['track-list']
    except (IndexError, TypeError, KeyError, ValueError) as e:
        print(e, f'could not find tracklist for {release_id}')
        return None
    tracklist = [track_info['recording']['title'] for track_info in tracklist]
    return tracklist
