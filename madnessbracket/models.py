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
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    title = db.Column(db.String(), nullable=False)
    rating = db.Column(db.Integer)
    alternative_title = db.Column(db.String())
    mb_id = db.Column(db.Integer)
    discogs_id = db.Column(db.Integer)
    release_date = db.Column(db.DateTime)
    album_cover_color = db.Column(db.String(), nullable=True)
    songs = db.relationship('Song', backref='album', lazy=True)

    def __repr__(self):
        return f"Album('{self.title}')"


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    spotify_preview_url = db.Column(db.String(), nullable=True)
    spotify_track_id = db.Column(db.String(), nullable=True)
    rating = db.Column(db.Integer)

    def __repr__(self):
        return f"Song('{self.title}')"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(200), unique=True, index=True, nullable=False)
    spotify_token = db.Column(db.String(200), unique=False, nullable=True)

    def __repr__(self):
        return f"User('{self.spotify_id}')"
