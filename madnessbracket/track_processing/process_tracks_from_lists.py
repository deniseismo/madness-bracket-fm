from madnessbracket.schemas.track_schema import TrackInfo


def process_tracks_from_info_list(tracks: list[dict[str]]) -> list[TrackInfo]:
    """
    processes tracks from info lists (list of dicts with all the needed info)
    :param tracks: (list[dict[str]]) a list of tracks info
    :return: (list[TrackInfo]) list of processed tracks (TrackInfo)
    """
    processed_tracks = []
    for track in tracks:
        track_info = process_a_track_from_info(track)
        processed_tracks.append(track_info)
    return processed_tracks


def process_a_track_from_info(track: dict[str]) -> TrackInfo:
    """
    process a track from info dict
    :param track: (dict[str]) information about the track
    :return: TrackInfo
    """
    track_info = TrackInfo(
        track_title=track["title"],
        artist_name=track["artist_name"],
        spotify_preview_url=track["preview_url"],
        album_colors=track["album_colors"],
        text_color=track["text_color"]
    )
    return track_info
