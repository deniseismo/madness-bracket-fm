from madnessbracket.models import Artist, Song


def get_tracks_from_db(artist_name: str):
    """
    :param artist_name: artist's name
    :return: a dict with a list of 'track info' dicts
    """
    SONG_LIMIT = 100
    artist = Artist.query.filter_by(name=artist_name).first()
    if not artist:
        # no such artist found
        return None

    track_entries = Song.query.filter_by(artist=artist).order_by(Song.rating).limit(SONG_LIMIT).all()

    if not track_entries:
        return None
    tracks = {
        "tracks": []
    }
    for counter, track_entry in enumerate(track_entries):
        track = {
            "id": counter,
            "title": track_entry.title,
            "artist_name": track_entry.artist.name,
            "album": track_entry.album.title,
            "color": track_entry.album.album_cover_color
        }
        if track_entry.spotify_preview_url:
            track['spotify_preview_url'] = track_entry.spotify_preview_url

        tracks["tracks"].append(track)
    return tracks
