from madnessbracket import db
from madnessbracket.dev.db_mgmt.album_mgmt.album_metadata_utilities import parse_release_date
from madnessbracket.models import Album


def add_new_album_to_database(artist_id: int, album_info: dict) -> bool:
    """
    add new album to database given artist's id (that's already been added to db) and album info
    Args:
        artist_id: (int) artist's id in database
        album_info: (dict) with album's information: rating, alternative title, mb_id, etc.

    """

    album_entry = Album(artist_id=artist_id, title=album_info["title"])
    if album_info["rating"]:
        album_entry.rating = album_info["rating"]
    if album_info["alternative_title"]:
        album_entry.alternative_title = album_info["alternative_title"]
    if album_info["mb_id"]:
        album_entry.mb_id = album_info["mb_id"]
    if album_info["discogs_id"]:
        album_entry.discogs_id = album_info["discogs_id"]
    if album_info["release_date"]:
        release_date = parse_release_date(album_info["release_date"])
        album_entry.release_date = release_date
    if album_info["album_cover_color"]:
        album_entry.album_cover_color = album_info["album_cover_color"]
    db.session.add(album_entry)
    db.session.commit()
    return True
