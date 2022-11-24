from madnessbracket import db
from madnessbracket.models import Artist


def add_new_artist_to_database(artist_name: str) -> bool:
    """
    """
    new_artist = Artist(name=artist_name)
    db.session.add(new_artist)
    db.session.commit()
    return True
