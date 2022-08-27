import asyncio
from typing import Optional

from madnessbracket import cache
from madnessbracket.music_apis.lastfm_api.lastfm_track_handlers import get_track_info_shortcut
from madnessbracket.music_apis.lastfm_api.lastfm_user_handlers import lastfm_get_user_top_tracks
from madnessbracket.music_apis.spotify_api.spotify_client_api import get_spotify_tekore_client
from madnessbracket.utilities.name_filtering import get_filtered_name
from madnessbracket.track_processing.track_preparation import prepare_tracks
from madnessbracket.track_processing.track_processing_helpers import add_text_color_to_tracks


def ultimate_lastfm_user_tracks_handler(username, upper_limit) -> Optional[dict]:
    """
    a shortcut function that ultimately returns randomized & processed lastfm user tracks with all the needed info
    :param username: user's name
    :param upper_limit: upper bracket limit
    :return: a dict with all the info about user's Last.fm tracks
    """
    correct_username, lastfm_user_top_tracks = lastfm_get_user_top_tracks(username)
    if not lastfm_user_top_tracks:
        print(f"COULD NOT find tracks for User({username})")
        return None
    capped_tracks = prepare_tracks(lastfm_user_top_tracks, upper_limit)
    tracks_with_info = get_lastfm_user_tracks_info(capped_tracks)
    print("TRACKS: ", tracks_with_info)
    add_text_color_to_tracks(tracks_with_info)
    tracks = {
        "tracks": tracks_with_info,
        "description": f"{correct_username}: My Last.fm",
        "value1": correct_username,
        "extra": None,
    }
    return tracks


@cache.memoize(timeout=36000)
def get_lastfm_user_tracks_info(tracks) -> list:
    """
    get all the info for the user's top tracks asynchronously
    :param tracks: a list of lastfm user's tracks
    :return: tracks with info
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tracks_with_info = asyncio.get_event_loop().run_until_complete(get_info_for_lastfm_user_tracks(tracks))
    print("RESULTS: ", tracks_with_info)
    return tracks_with_info


async def get_info_for_lastfm_user_tracks(tracks):
    """
    an async function that tries to find all the necessary info about user's tracks: album, cover art color, etc.
    :param tracks: a list of lastfm user tracks
    :return: a future aggregating results (tracks with all the info needed)
    """
    tasks = []
    tekore_client = get_spotify_tekore_client(asynchronous=True)
    for track in tracks:
        try:
            artist_name = track['artist']['name']
            track_title = get_filtered_name(track['name'])
        except (KeyError, ValueError) as e:
            print("error when parsing lastfm tracks", e)
            continue
        task = asyncio.create_task(get_track_info_shortcut(track_title, artist_name, tekore_client))
        tasks.append(task)
    return await asyncio.gather(*tasks)
