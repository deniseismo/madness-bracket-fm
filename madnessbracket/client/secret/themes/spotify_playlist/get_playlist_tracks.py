import os

from flask import current_app

from madnessbracket.schemas.response import TracksInfoResponse
from madnessbracket.track_processing.process_tracks_from_lists import process_tracks_from_info_list
from madnessbracket.track_processing.track_preparation import prepare_tracks
from madnessbracket.track_processing.track_processing_helpers import make_tracks_info_response, load_tracks_from_file


def get_seismo_top_tracks_of_2021(bracket_limit: int) -> TracksInfoResponse:
    """
    get seismo's top tracks of 2021
    :param bracket_limit: (int) bracket's upper limit
    :return: (TracksInfoResponse) with all the secret theme bracket info
    """
    seismo_top_2021_tracks = _load_seismo_top_tracks_of_2021_from_file()
    processed_tracks = process_tracks_from_info_list(seismo_top_2021_tracks)
    prepared_tracks = prepare_tracks(processed_tracks, bracket_limit)
    title = "SEISMO'S TOP SONGS OF 2021"
    tracks_info_response = make_tracks_info_response(
        tracks=prepared_tracks,
        description=title,
        extra=None
    )
    return tracks_info_response


def _load_seismo_top_tracks_of_2021_from_file() -> list[dict[str]]:
    """
    load seismo's top tracks from .json
    :return: (list[dict[str]]) with all the info about tracks
    """
    filename = "seismo_top_2021.json"
    filepath = os.path.join(current_app.root_path, "client/secret/themes/spotify_playlist", filename)
    seismo_top_2021_tracks = load_tracks_from_file(filepath)
    return seismo_top_2021_tracks
