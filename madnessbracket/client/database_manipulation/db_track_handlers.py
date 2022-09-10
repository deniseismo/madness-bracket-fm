from typing import Optional

from sqlalchemy.event import listen

from madnessbracket import db
from madnessbracket.models import Artist, Song
from madnessbracket.utilities.db_extensions import load_unicode_extension
from madnessbracket.utilities.logging_handlers import log_arbitrary_data


def db_get_tracks_by_artist_entry(artist_entry: Artist, max_songs_range: int = 100) -> Optional[list[Song]]:
    """
    get artist's tracks from database (given Artist from db); sorted by rating (that is the most popular ones)
    :param artist_entry: (Artist) artist found in database
    :param max_songs_range: (int) maximum number of top songs to choose from, defaults to top 100
    :return: (list[Song]) Songs (tracks) by Artist from db
    """
    track_entries = Song.query.filter_by(artist=artist_entry).order_by(Song.rating.desc()).limit(max_songs_range).all()
    if not track_entries:
        return None
    return track_entries


def db_get_track_by_name(track_title: str, artist_name: str) -> Optional[Song]:
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
