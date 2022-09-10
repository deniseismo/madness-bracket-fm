import os

from flask import current_app

from madnessbracket.schemas.response import TracksInfoResponse
from madnessbracket.track_processing.process_tracks_from_lists import process_tracks_from_info_list
from madnessbracket.track_processing.track_preparation import prepare_tracks
from madnessbracket.track_processing.track_processing_helpers import make_tracks_info_response, load_tracks_from_file


def get_secret_eurovision_tracks(bracket_limit: int) -> TracksInfoResponse:
    """
    get EUROVISION 2021 tracks
    :param bracket_limit: (int) bracket's upper limit
    :return: (TracksInfoResponse) with all the secret theme bracket info
    """
    eurovision_tracks = _load_eurovision_tracks_from_file()
    processed_tracks = process_tracks_from_info_list(eurovision_tracks)
    prepared_tracks = prepare_tracks(processed_tracks, bracket_limit)
    title = "Eurovision 2021"
    tracks_info_response = make_tracks_info_response(
        tracks=prepared_tracks,
        description=title.upper(),
        extra=None
    )
    return tracks_info_response


def _load_eurovision_tracks_from_file() -> list[dict[str]]:
    """
    load eurovision tracks from .json
    :return: (list[dict[str]]) with all the info about tracks
    """
    filename = "eurovision_2021.json"
    filepath = os.path.join(current_app.root_path, "client/secret/themes/eurovision", filename)
    eurovision_tracks = load_tracks_from_file(filepath)
    return eurovision_tracks
