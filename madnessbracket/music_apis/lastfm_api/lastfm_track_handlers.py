from aiocache import cached, Cache
from aiocache.serializers import PickleSerializer
from sqlalchemy.event import listen

from madnessbracket import db
from madnessbracket.music_apis.lastfm_api.lastfm_api import lastfm_get_response
from madnessbracket.music_apis.spotify_api.spotify_async_track_handlers import fetch_spotify_track_info
from madnessbracket.models import Song, Artist
from madnessbracket.track_processing.process_tracks_from_spotify import process_a_track_from_spotify
from madnessbracket.track_processing.process_tracks_from_database import process_a_track_from_db
from madnessbracket.utilities.db_extensions import load_unicode_extension
from madnessbracket.utilities.logging_handlers import log_arbitrary_data


def find_track_in_database(track_title: str, artist_name: str):
    """
    find a particular track (Song instance) in database
    :param track_title: track's title
    :param artist_name: artist's name
    :return: (Song) a Song instance
    """
    listen(db.engine, 'connect', load_unicode_extension)
    song_in_database = db.session.query(Song). \
        join(Artist).filter(Artist.name.like(artist_name)). \
        filter(Song.title.like(track_title)).first()
    if not song_in_database:
        print(
            f"COULD NOT find: Track({track_title}) by Artist({artist_name}) in database")
        log_arbitrary_data(f"Track({track_title}) by Artist({artist_name})", "lastfm_tracks_not_found_in_db.csv")
        return None
    return song_in_database


@cached(ttl=3600, serializer=PickleSerializer(), cache=Cache.MEMORY)
async def get_track_info_shortcut(track_title: str, artist_name: str, spotify_tekore_client):
    """
    a shortcut function that combines two methods of finding track info: database and spotify
    used for finding track info in lastfm user's top tracks
    :param track_title: track's title
    :param artist_name: artist's name
    :param spotify_tekore_client: an async spotify API client
    :return: a dict with all the track's info
    """
    if not track_title or not artist_name:
        return None
    track = find_track_in_database(track_title, artist_name)
    if not track:
        track = await fetch_spotify_track_info(track_title, artist_name, spotify_tekore_client)
        print(track)
        if not track:
            print(
                f"NO SPOTIFY TRACK INFO for Artist({artist_name}) — Track({track_title})")
            return {
                "track_title": track_title,
                "artist_name": artist_name,
                "spotify_preview_url": None,
                "album_colors": None
            }
        track_info = process_a_track_from_spotify(track)
        return track_info

    track_info = process_a_track_from_db(track)
    return track_info


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
        print(f"couldn't find {track_title} by {artist_name} on last.fm")
        return None
    try:
        track_playcount = response.json()['track']['playcount']

    except (KeyError, IndexError, TypeError, ValueError) as e:
        print(e)
        print(f"no one seemed to listen for {track_title}")
        return 0
    return int(track_playcount)
