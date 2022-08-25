from madnessbracket.models import Song
from madnessbracket.schemas.track_schema import TrackInfo


def process_tracks_from_db(track_entries: list[Song]) -> list[TrackInfo]:
    """
    process track entries (Song) from database
    :param track_entries: (list[Song] a list of track entries (Songs) from db
    :return: (list[TrackInfo]) a list of processed TracInfo tracks with all the information needed;
    (well, except for text colors that will be calculated later for a capped & randomized list of tracks to save time)
    """
    processed_tracks = []
    for track_entry in track_entries:
        track = process_a_track_from_db(track_entry)
        processed_tracks.append(track)
    return processed_tracks


def process_a_track_from_db(track_entry: Song) -> TrackInfo:
    """
    gets all the needed info about the track from track entry (Song object)
    :param track_entry: (Song) a Song instance
    :return: (TrackInfo)
    """
    track_info = TrackInfo(
        track_title=track_entry.title,
        artist_name=track_entry.artist.name
    )
    if track_entry.spotify_preview_url:
        track_info.spotify_preview_url = track_entry.spotify_preview_url
    album_colors = track_entry.album.get_list_of_album_colors()
    if album_colors:
        track_info.album_colors = album_colors
    return track_info
