from madnessbracket.schemas.track_schema import TrackInfo


def process_tracks_from_charts(tracks: list[dict[str]]) -> list[TrackInfo]:
    """
    processes tracks from charts lists (list of dicts with all the needed info)
    :param tracks: (list[dict[str]]) a list of tracks from charts
    :return: (list[TrackInfo]) list of processed tracks (TrackInfo)
    """
    processed_tracks = []
    for track in tracks:
        track_info = process_a_track_from_charts(track)
        processed_tracks.append(track_info)
    return processed_tracks


def process_a_track_from_charts(track: dict[str]) -> TrackInfo:
    """
    process a track from charts list
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
