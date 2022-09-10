import os

from flask import current_app

from madnessbracket.schemas.response import TracksInfoResponse
from madnessbracket.track_processing.process_tracks_from_lists import process_tracks_from_info_list
from madnessbracket.track_processing.track_preparation import prepare_tracks
from madnessbracket.track_processing.track_processing_helpers import make_tracks_info_response, load_tracks_from_file


def get_secret_number_tracks(bracket_limit: int) -> TracksInfoResponse:
    """
    get NUMBER tracks (tracks with number in the title)
    :param bracket_limit: (int) bracket's upper limit
    :return: (TracksInfoResponse) with all the secret theme bracket info
    """
    number_tracks = _load_number_tracks_from_file()
    processed_tracks = process_tracks_from_info_list(number_tracks)
    prepared_tracks = prepare_tracks(processed_tracks, bracket_limit)
    title = "number numbers"
    tracks_info_response = make_tracks_info_response(
        tracks=prepared_tracks,
        description=title,
        extra=None
    )
    return tracks_info_response


def _load_number_tracks_from_file() -> list[dict[str]]:
    """
    load number tracks from .json
    :return: (list[dict[str]]) with all the info about tracks
    """
    filename = "tracks_with_numbers.json"
    filepath = os.path.join(current_app.root_path, "client/secret/themes/pattern_in_the_title", filename)
    number_tracks = load_tracks_from_file(filepath)
    return number_tracks
