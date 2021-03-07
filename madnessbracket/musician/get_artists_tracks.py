from madnessbracket.models import Artist, Song


def get_artists_tracks(artist_name: str):
    """
    :param artist_name: artist's name
    :return: a dict with a list of 'track info' dicts
    """
    SONG_LIMIT = 50
    artist = Artist.query.filter_by(name=artist_name).first()
    if not artist:
        # no such artist found
        return None

    track_entries = Song.query.filter_by(artist=artist).order_by(Song.rating.desc()).limit(SONG_LIMIT).all()

    if not track_entries:
        return None
    tracks = {
        "tracks": []
    }
    for track_entry in track_entries:
        track = {
            "track_title": track_entry.title,
            "artist_name": track_entry.artist.name,
            "spotify_preview_url": track_entry.spotify_preview_url if track_entry.spotify_preview_url else None
        }
        tracks["tracks"].append(track)
    return tracks