from typing import Optional

from sqlalchemy import JSON

from madnessbracket import db


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, index=True, nullable=False)
    albums = db.relationship('Album', backref='artist', lazy=True)
    spotify_name = db.Column(db.String(), nullable=True)
    songs = db.relationship('Song', backref='artist', lazy=True)

    def __repr__(self):
        return f"Artist('{self.name}')"


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artist.id'), nullable=False)
    title = db.Column(db.String(), nullable=False)
    rating = db.Column(db.Integer)
    alternative_title = db.Column(db.String())
    mb_id = db.Column(db.Integer)
    discogs_id = db.Column(db.Integer)
    release_date = db.Column(db.DateTime)
    album_cover_color = db.Column(db.String(), nullable=True)
    songs = db.relationship('Song', backref='album', lazy=True)

    def __repr__(self):
        album_description = f"Album({self.title})"
        if self.artist:
            album_description += f" by Artist({self.artist.name})"
        return album_description

    def get_list_of_album_colors(self) -> Optional[list[str]]:
        if not self.album_cover_color:
            return None
        try:
            list_of_album_colors = self.album_cover_color.split(",")
            print(f"{list_of_album_colors=}")
            return list_of_album_colors
        except AttributeError as e:
            print(e)
            return None


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artist.id'), nullable=False)
    spotify_preview_url = db.Column(db.String(), nullable=True)
    spotify_track_id = db.Column(db.String(), nullable=True)
    rating = db.Column(db.Integer)

    def __repr__(self):
        song_description = f"Song({self.title})"
        if self.artist:
            song_description += f" by Artist({self.artist.name})"
        return song_description


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(200), unique=True,
                           index=True, nullable=False)
    spotify_token = db.Column(db.String(200), unique=False, nullable=True)

    def __repr__(self):
        return f"User('{self.spotify_id}')"


class BracketData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bracket_id = db.Column(db.String(), unique=True,
                           index=True, nullable=False)
    bracket_type = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(), nullable=False)
    value1 = db.Column(db.String(), nullable=True)
    value2 = db.Column(db.String(), nullable=True)
    extra = db.Column(db.String(), nullable=True)
    bracket_info = db.Column(JSON, nullable=False)
    winner = db.Column(db.String(), nullable=True)

    def __repr__(self):
        return f"Bracket('{self.bracket_id}') — {self.title}"
