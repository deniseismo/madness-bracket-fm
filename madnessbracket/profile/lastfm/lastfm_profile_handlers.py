import asyncio

from madnessbracket import cache
from madnessbracket.dev.lastfm.lastfm_track_handlers import get_track_info_shortcut
from madnessbracket.dev.lastfm.lastfm_user_handlers import lastfm_get_user_top_tracks
from madnessbracket.dev.spotify.spotify_client_api import get_spotify_tekore_client
from madnessbracket.profile.lastfm.prepare_tracks import prepare_tracks_for_lastfm_profile


def ultimate_lastfm_user_tracks_handler(username, upper_limit):
    """
    a shortcut function that ultimately returns randomized & processed lastfm user tracks with all the needed info
    :param username: user's name
    :param upper_limit: upper bracket limit
    :return:
    """
    lastfm_user_top_tracks = lastfm_get_user_top_tracks(username)
    if not lastfm_user_top_tracks:
        print(f"COULD NOT find tracks for User({username})")
        return None
    capped_tracks = prepare_tracks_for_lastfm_profile(lastfm_user_top_tracks, upper_limit)
    tracks_with_info = get_lastfm_user_tracks_info(capped_tracks)
    print("TRACKS: ", tracks_with_info)
    tracks = {
        "tracks": tracks_with_info,
        "description": f"{username}",
        "secret": None,
    }
    return tracks


@cache.memoize(timeout=36000)
def get_lastfm_user_tracks_info(tracks):
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
            track_title = track['name']
        except (KeyError, ValueError) as e:
            print("error when parsing lastfm tracks", e)
            continue
        task = asyncio.create_task(get_track_info_shortcut(track_title, artist_name, tekore_client))
        tasks.append(task)
    return await asyncio.gather(*tasks)
