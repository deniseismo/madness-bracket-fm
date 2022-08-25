from typing import Optional

from sqlalchemy.event import listen

from madnessbracket import db
from madnessbracket.models import Artist
from madnessbracket.utilities.db_extensions import load_unicode_extension


def db_get_artist(artist_name: str) -> Optional[Artist]:
    """
    get artist from database
    :param artist_name: (str) artist's name
    :return: (Artist) from database
    """
    listen(db.engine, 'connect', load_unicode_extension)
    artist_entry = Artist.query.filter(Artist.name.like(artist_name)).first()
    if not artist_entry:
        return None
    return artist_entry
