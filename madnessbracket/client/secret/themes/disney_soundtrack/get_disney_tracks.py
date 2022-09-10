import os

from flask import current_app

from madnessbracket.schemas.response import TracksInfoResponse
from madnessbracket.track_processing.process_tracks_from_lists import process_tracks_from_info_list
from madnessbracket.track_processing.track_preparation import prepare_tracks
from madnessbracket.track_processing.track_processing_helpers import make_tracks_info_response, load_tracks_from_file


def get_secret_disney_tracks(bracket_limit: int) -> TracksInfoResponse:
    """
    get Disney Soundtrack hits
    :param bracket_limit: (int) bracket's upper limit
    :return: (TracksInfoResponse) with all the secret theme bracket info
    """
    disney_tracks = _load_disney_tracks_from_file()
    processed_disney_tracks = process_tracks_from_info_list(disney_tracks)
    prepared_disney_tracks = prepare_tracks(processed_disney_tracks, bracket_limit)
    title = "Disney Soundtrack"
    tracks_info_response = make_tracks_info_response(
        tracks=prepared_disney_tracks,
        description=title.upper(),
        extra=None
    )
    return tracks_info_response


def _load_disney_tracks_from_file() -> list[dict[str]]:
    """
    load disney tracks from .json
    :return: (list[dict[str]]) with all the info about tracks
    """
    filename = "disney_soundtrack.json"
    filepath = os.path.join(current_app.root_path, "client/secret/themes/disney_soundtrack", filename)
    disney_tracks = load_tracks_from_file(filepath)
    return disney_tracks
