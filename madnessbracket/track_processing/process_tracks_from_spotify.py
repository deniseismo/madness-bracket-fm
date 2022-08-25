from tekore._model import FullTrack

from madnessbracket.dev.db_mgmt.color_mgmt.dominant_colors import get_image_dominant_colors_via_image_url
from madnessbracket.schemas.track_schema import TrackInfo
from madnessbracket.utilities.name_filtering import get_filtered_name


def process_tracks_from_spotify(tracks: list[FullTrack]) -> list[TrackInfo]:
    """
    process tracks from Spotify
    :param tracks: (list[FullTrack]) a list of tracks from Spotify
    :return: (list[TrackInfo]) a list of processed tracks (TrackInfo) from Spotify
    """
    processed_tracks = []
    track_titles = set()
    for track_entry in tracks:
        track_title = get_filtered_name(track_entry.name)
        if track_title in track_titles:
            continue
        track_titles.add(track_title)
        track_info = process_a_track_from_spotify(track_entry)
        track_info.track_title = track_title
        processed_tracks.append(track_info)
    return processed_tracks


def process_a_track_from_spotify(track_entry: FullTrack) -> TrackInfo:
    """
    gets all the needed info about the track from track entry (FullTrack tekore object)
    :param track_entry: a FullTrack tekore instance
    :return: (TrackInfo) processed track from spotify
    """
    try:
        album_image_url = track_entry.album.images[-1].url
        album_colors = get_image_dominant_colors_via_image_url(album_image_url)
    except (IndexError, ValueError) as e:
        print(e)
        album_colors = None
    track_info = TrackInfo(
        track_title=track_entry.name,
        artist_name=track_entry.artists[0].name
    )
    if track_entry.preview_url:
        track_info.spotify_preview_url = track_entry.preview_url
    if album_colors:
        track_info.album_colors = album_colors
    return track_info
