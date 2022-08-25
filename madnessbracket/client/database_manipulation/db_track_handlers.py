from typing import Optional

from madnessbracket.models import Artist, Song


def db_get_tracks_by_artist_entry(artist_entry: Artist) -> Optional[list[Song]]:
    """
    get artist's tracks from database (given Artist from db); sorted by rating (that is the most popular ones)
    :param artist_entry: (Artist) artist found in database
    :return: (list[Song]) Songs (tracks) by Artist from db
    """
    SONG_LIMIT = 100
    track_entries = Song.query.filter_by(artist=artist_entry).order_by(Song.rating.desc()).limit(SONG_LIMIT).all()
    if not track_entries:
        return None
    return track_entries
