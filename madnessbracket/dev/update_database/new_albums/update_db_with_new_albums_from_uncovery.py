import csv
import os

from flask import current_app

from madnessbracket import create_app
from madnessbracket.dev.dev_db_manipulation.dev_db_album_handlers import add_new_album_to_database
from madnessbracket.dev.dev_db_manipulation.dev_db_artist_handlers import add_new_artist_to_database
from madnessbracket.models import Artist

app = create_app()
app.app_context().push()


def add_new_albums_from_uncovery_info_csv() -> None:
    """
    add new albums (and artists if necessary) from a transfer .csv file
    (created beforehand based on the info taken from  my uncovery db)
    """
    TRANSFER_ALBUMS_FOLDER = 'dev/update_database/new_albums'
    TRANSFER_ALBUMS_FILENAME = "transfer_new_albums.csv"
    TRANSFER_ALBUMS_PATH = os.path.join(current_app.root_path, TRANSFER_ALBUMS_FOLDER, TRANSFER_ALBUMS_FILENAME)
    with open(TRANSFER_ALBUMS_PATH, encoding="utf-8") as file:
        album_infos = csv.DictReader(file)
        for album_info in album_infos:
            artist_name = album_info["artist"]
            artist_entry = Artist.query.filter(Artist.name == artist_name).first()
            if artist_entry:
                artist_id = artist_entry.id
            else:
                print("ARTIST NOT FOUND")
                print(f"adding NEW artist: {artist_name}")
                add_new_artist_to_database(artist_name)
                artist_entry = Artist.query.filter(Artist.name == artist_name).first()
                artist_id = artist_entry.id

            add_new_album_to_database(artist_id, album_info)
