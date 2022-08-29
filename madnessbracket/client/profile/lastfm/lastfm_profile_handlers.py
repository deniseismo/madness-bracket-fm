import asyncio
from typing import Optional

import tekore as tk
from aiocache import cached, Cache
from aiocache.serializers import PickleSerializer

from madnessbracket.client.database_manipulation.db_track_handlers import db_get_track_by_name
from madnessbracket.music_apis.lastfm_api.lastfm_user_handlers import lastfm_get_user_top_tracks_info
from madnessbracket.music_apis.spotify_api.spotify_async_track_handlers import fetch_spotify_track_info
from madnessbracket.music_apis.spotify_api.spotify_client_api import get_spotify_tekore_client
from madnessbracket.schemas.lastfm_user_info import LastFMUserTopTracksProcessedInfo
from madnessbracket.schemas.track_schema import TrackInfo
from madnessbracket.track_processing.process_tracks_from_database import process_a_track_from_db
from madnessbracket.track_processing.process_tracks_from_spotify import process_a_track_from_spotify
from madnessbracket.track_processing.track_preparation import prepare_tracks
from madnessbracket.track_processing.track_processing_helpers import add_text_color_to_tracks


def get_tracks_for_lastfm_user(username: str, upper_limit: int = 16) -> Optional[LastFMUserTopTracksProcessedInfo]:
    """
    get tracks for profile: last.fm;
    processed & ready info for user's tracks as well as user's corrected username (the way it's stylized)
    :param username: (str) username on last.fm
    :param upper_limit: (int) bracket upper limit
    :return: (LastFMUserTopTracksProcessedInfo) with username (corrected stylized form)
        and their tracks with all the needed info
    """
    top_tracks_info = lastfm_get_user_top_tracks_info(username)
    if not top_tracks_info:
        print(f"--no tracks on last.fm for User({username})")
        return None
    top_tracks_info.tracks = prepare_tracks(top_tracks_info.tracks, upper_limit)
    top_tracks_info.tracks = get_lastfm_user_tracks_with_additional_info(top_tracks_info.tracks)
    add_text_color_to_tracks(top_tracks_info.tracks)
    return top_tracks_info


def get_lastfm_user_tracks_with_additional_info(tracks: list[TrackInfo]) -> list[TrackInfo]:
    """
    get additional information for tracks found on last.fm: spotify preview url, album colors, etc.
    :param tracks: (list[TrackInfo]) a list of lastfm user's tracks (processed as TrackInfo objects)
    :return: (list[TrackInfo]) list of TrackInfo tracks with added info
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tracks_with_info = asyncio.get_event_loop().run_until_complete(get_additional_info_for_lastfm_user_tracks(tracks))
    return tracks_with_info


async def get_additional_info_for_lastfm_user_tracks(tracks: list[TrackInfo]):
    """
    an async function that tries to find additional info about last.fm user's tracks: album, cover art color, etc.
    :param tracks: (list[TrackInfo]) a list of lastfm user tracks (processed as TrackInfo objects)
    :return: a future aggregating results (tracks with all the info needed)
    """
    tasks = []
    tekore_client = get_spotify_tekore_client(asynchronous=True)
    if not tekore_client:
        return None
    for track_info in tracks:
        task = asyncio.create_task(
            get_additional_info_for_a_lastfm_user_track(
                track_info.track_title,
                track_info.artist_name,
                tekore_client
            )
        )
        tasks.append(task)
    return await asyncio.gather(*tasks)


@cached(ttl=3600, serializer=PickleSerializer(), cache=Cache.MEMORY)
async def get_additional_info_for_a_lastfm_user_track(
        track_title: str,
        artist_name: str,
        spotify_tekore_client: tk.Spotify
) -> Optional[TrackInfo]:
    """
    gets additional information for a last.fm user track via db & spotify
    :param track_title: track's title
    :param artist_name: artist's name
    :param spotify_tekore_client: (tk.Spotify) an async spotify API client
    :return: (TrackInfo) with added info
    """
    if not track_title or not artist_name:
        return None
    track = db_get_track_by_name(track_title, artist_name)
    if not track:
        track = await fetch_spotify_track_info(track_title, artist_name, spotify_tekore_client)
        print(track)
        if not track:
            print(f"--no spotify info for Artist({artist_name}) — Track({track_title})")
            return TrackInfo(
                track_title=track_title,
                artist_name=artist_name,
            )
        track_info = process_a_track_from_spotify(track)
        return track_info
    track_info = process_a_track_from_db(track)
    return track_info
