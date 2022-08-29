import json
import random
from typing import Optional

from madnessbracket.music_apis.lastfm_api.exceptions import LastFMNotEnoughTracksError, LastFMCriticalError
from madnessbracket.music_apis.lastfm_api.lastfm_api import lastfm_get_response
from madnessbracket.music_apis.lastfm_api.lastfm_helpers import lastfm_show_response_error
from madnessbracket.schemas.lastfm_user_info import LastFMUserTopTracksInfo, LastFMPaginationInfo, \
    LastFMUserTopTracksProcessedInfo
from madnessbracket.track_processing.process_tracks_from_lastfm import process_tracks_from_lastfm


def lastfm_get_user_top_tracks_info(username: str) -> Optional[LastFMUserTopTracksProcessedInfo]:
    """
    get information about user's top tracks for a chosen (randomly, for now) time period;
    LastFMUserTopTracksProcessedInfo
    :param username: (str) username on last.fm
    :return: (LastFMUserTopTracksProcessedInfo) with corrected username & processed tracks from last.fm
    """
    TIME_PERIODS = [
        "overall",
        "7day",
        "1month",
        "3month",
        "6month",
        "12month"
    ]
    time_period = random.choice(TIME_PERIODS)
    print(f"{time_period=}")
    try:
        user_tracks_info = _lastfm_collect_user_tracks_info(username, time_period)
    # in case of incorrect username or some more serious errors return None right away
    except LastFMCriticalError as e:
        print(e)
        return None
    # no (or too few) tracks found for a chosen time period, we might try to find tracks using 'overall' as time period
    except LastFMNotEnoughTracksError as e:
        print(e)
        try:
            print(f"could not find tracks for {username} for {time_period=}, trying to find tracks 'overall'")
            user_tracks_info = _lastfm_collect_user_tracks_info(username, time_period="overall")
        except (LastFMCriticalError, LastFMNotEnoughTracksError) as e:
            print(e)
            return None
    if not user_tracks_info:
        return None
    processed_user_tracks = process_tracks_from_lastfm(user_tracks_info.tracks)
    lastfm_user_top_tracks_processed_info = LastFMUserTopTracksProcessedInfo(
        username=user_tracks_info.username,
        tracks=processed_user_tracks
    )
    return lastfm_user_top_tracks_processed_info


def _lastfm_collect_user_tracks_info(
        username: str,
        time_period: str
) -> Optional[LastFMUserTopTracksInfo]:
    """
    collects all the tracks info from last.fm; combines info from several 'pages' of last.fm response
    (last.fm gives out only 50 tracks per page/request)
    :param username: (str) lastfm username
    :param time_period: (str) time period chosen
    :return: (LastFMUserTopTracksInfo) with all the collected info: username & top tracks (unprocessed)
    """
    MAX_PAGES = 3
    page = 1
    tracks_list = []
    for _ in range(MAX_PAGES):
        user_tracks_info = _lastfm_get_user_tracks_info_for_specific_time_period(username, time_period, page)
        if not user_tracks_info:
            break
        pagination_info = _get_pagination_info_from_lastfm_user_tracks_info(user_tracks_info)
        if not pagination_info:
            break
        page, total_pages = pagination_info
        total_pages_limit = min(total_pages, MAX_PAGES)
        tracks = _get_tracks_from_lastfm_user_tracks_info(user_tracks_info)
        if not tracks:
            break
        tracks_list.extend(tracks)
        if page == 1:
            correct_username = _get_correct_username_from_lastfm_user_tracks_info(user_tracks_info)
            if correct_username:
                username = correct_username
        page += 1
        if page > total_pages_limit:
            break

    if not tracks_list:
        return None
    top_tracks_info = LastFMUserTopTracksInfo(
        username=username,
        tracks=tracks_list
    )
    return top_tracks_info


def _get_tracks_from_lastfm_user_tracks_info(user_tracks_info: dict[str]) -> Optional[list[dict[str]]]:
    """
    parse last.fm user tracks info to get all the tracks from it
    :param user_tracks_info: (dict[str]) track's info from last.fm (json() from response)
    :return: (list[dict[str]]) a list of tracks info from last.fm
    """
    try:
        tracks = user_tracks_info["toptracks"]["track"]
    except (KeyError, TypeError) as e:
        return None
    return tracks


def _get_correct_username_from_lastfm_user_tracks_info(user_tracks_info: dict[str]) -> Optional[str]:
    """
    parse last.fm user tracks info to get user's corrected name (the way it's stylized)
    :param user_tracks_info: (dict[str])track's info from last.fm (json() from response)
    :return: (str) username (correct spelling, stylization)
    """
    try:
        correct_username = user_tracks_info['toptracks']['@attr']['user']
        return correct_username
    except (KeyError, ValueError, TypeError) as e:
        print(e)
        return None


def _get_pagination_info_from_lastfm_user_tracks_info(user_tracks_info: dict[str]) -> Optional[LastFMPaginationInfo]:
    """
    parse last.fm user tracks info to get current page and total number of pages
    :param user_tracks_info: (dict[str])track's info from last.fm (json() from response)
    :return: (LastFMPaginationInfo) with current page and total number of pages
    """
    try:
        page = int(user_tracks_info['toptracks']['@attr']['page'])
        total_pages = int(user_tracks_info['toptracks']['@attr']['totalPages'])
    except (KeyError, TypeError) as e:
        print(e)
        return None
    return LastFMPaginationInfo(page=page, total_pages=total_pages)


def _lastfm_get_user_tracks_info_for_specific_time_period(
        username: str,
        time_period: str,
        page: int = 1,
) -> Optional[dict]:
    """
    get lastfm user tracks info for time period (and page) chosen
    :param username: (str) lastfm username
    :param time_period: (str) time period chosen
    :param page: (int) number of the page (as a sort of offset);
        as last.fm gives out only 50 tracks (at most) per request
    :return: (dict) tracks info from last.fm
    """
    PER_PAGE_LIMIT = 50
    response = lastfm_get_response({
        'method': 'user.getTopTracks',
        'user': username,
        'period': time_period,
        'limit': PER_PAGE_LIMIT,
        'page': page
    })
    print(f"{response=} after")
    if response is None:
        raise LastFMCriticalError("no response")
    if response.status_code != 200:
        lastfm_show_response_error(response)
        raise LastFMCriticalError("critical last.fm error")
    try:
        lastfm_user_tracks_info = response.json()
    except json.decoder.JSONDecodeError as e:
        print(e)
        return None
    total_number_of_tracks = _get_total_number_of_tracks_from_lastfm_user_tracks_info(lastfm_user_tracks_info)
    if total_number_of_tracks < 4:
        raise LastFMNotEnoughTracksError(f"{total_number_of_tracks=}")
    return lastfm_user_tracks_info


def _get_total_number_of_tracks_from_lastfm_user_tracks_info(user_tracks_info: dict[str]) -> Optional[int]:
    """
    parse last.fm user tracks info to get total number of tracks user has for the time period chosen
    :param user_tracks_info: (dict[str])track's info from last.fm (json() from response)
    :return: (int) total number of tracks
    """
    try:
        total_number_of_tracks = int(user_tracks_info['toptracks']['@attr']['total'])
        return total_number_of_tracks
    except (KeyError, ValueError, TypeError) as e:
        print(e)
        return None
