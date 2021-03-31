from urllib.error import HTTPError
import musicbrainzngs
import requests_cache
from musicbrainzngs.musicbrainz import ResponseError
from flask import current_app
from madnessbracket import create_app
from madnessbracket.utilities.logging_handlers import log_missing_info

app = create_app()
app.app_context().push()


requests_cache.install_cache()

musicbrainzngs.set_useragent(
    *current_app.config['MUSIC_BRAINZ_USER_AGENT'].split(','))


def music_brainz_get_release_id_via_release_group(release_group_id: str):
    """get release id from a release_group id
    param:
        release_group_id (str): release group id from Music Brainz

    return:
        (str): release id
    """
    try:
        release_group_info = musicbrainzngs.get_release_group_by_id(
            release_group_id, includes=['releases'])
    except (HTTPError, ResponseError) as e:
        info = f"RELEASE GROUP ID ({release_group_id}   ERROR({e}))"
        log_missing_info(info)
        print(f'a response error occurred for {release_group_id}', e)
        return None
    try:
        release_id = release_group_info['release-group']['release-list'][0]['id']
    except (IndexError, KeyError, TypeError, ValueError) as e:
        print(f"couldn't find release id for {release_group_id}", e)
        return None
    print(release_id)
    return release_id


def music_brainz_get_release_tracklist(release_id: str):
    """get release group info by it id
    :param 
        release_group_id (str): release group id from Music Brainz
    :return: 
        (list) a list of tracks (track titles) for the current release (album)
    """
    try:
        release_info = musicbrainzngs.get_release_by_id(
            release_id, includes=['media', 'recordings'])
    except (HTTPError, ResponseError) as e:
        print(f'a response error occurred for {release_id}', e)
        return None
    if not release_info:
        print(f'no release info returned for {release_id}')
        return None
    try:
        tracklist = []
        for album_cd in release_info['release']['medium-list']:
            tracklist += album_cd['track-list']
    except (IndexError, TypeError, KeyError, ValueError) as e:
        print(e, f'could not find tracklist for {release_id}')
        return None
    tracklist = [track_info['recording']['title'] for track_info in tracklist]
    return tracklist


def music_brainz_get_release_tracklist_b_sides(release_id: str):
    """extra function: GET ONLY B-SIDES, CD2, etc, skipping CD1 in medium-list
    :param 
        release_group_id (str): release group id from Music Brainz
    :return: 
        (list) a list of tracks (track titles) for the current release (album)
    """
    try:
        release_info = musicbrainzngs.get_release_by_id(
            release_id, includes=['media', 'recordings'])
    except (HTTPError, ResponseError) as e:
        print(f'a response error occurred for {release_id}', e)
        return None
    if not release_info:
        print(f'no release info returned for {release_id}')
        return None
    try:
        tracklist = []
        if len(release_info['release']['medium-list']) > 1:
            for album_cd in release_info['release']['medium-list'][1:]:
                tracklist += album_cd['track-list']
        else:
            print("ONLY 1 CD FOUND")
            return None
    except (IndexError, TypeError, KeyError, ValueError) as e:
        print(e, f'could not find tracklist for {release_id}')
        return None
    tracklist = [track_info['recording']['title'] for track_info in tracklist]
    return tracklist
