import json
import os
import random
from typing import Optional

from flask import current_app

from madnessbracket import cache
from madnessbracket.schemas.track_schema import TrackInfo
from madnessbracket.track_processing.process_tracks_from_charts import process_tracks_from_charts
from madnessbracket.track_processing.track_preparation import prepare_tracks


def get_tracks_for_charts(bracket_upper_limit: int) -> Optional[list[TrackInfo]]:
    """
    get charts tracks
    :param bracket_upper_limit: (int) bracket upper limit size
    :return: (list[TrackInfo]) list of charts TrackInfo (processed & prepared tracks)
    """
    charts_filename = _pick_charts_list()
    songs = load_charts_list_from_the_file(charts_filename)
    if not songs:
        return None
    processed_tracks = process_tracks_from_charts(songs)
    prepared_tracks = prepare_tracks(processed_tracks, bracket_upper_limit)
    return prepared_tracks


@cache.memoize(timeout=36000)
def load_charts_list_from_the_file(charts_filename: str) -> Optional[list[dict[str]]]:
    """
    load songs considered best from file
    :return: (list[dict[str]]) list of dicts with all the info
    """
    filepath = os.path.join(current_app.root_path, 'client', 'charts', 'charts_lists', 'ready', charts_filename)
    try:
        with open(filepath, encoding='utf-8') as f:
            songs = json.load(f)
    except IOError as e:
        print('file not found', e)
        return None
    return songs


def _pick_charts_list() -> str:
    """
    pick a random charts list from a list of available charts (filenames of the charts)
    :return: (str) charts list filename
    """
    charts_lists_filenames = ['nme_top_500_extended.json', "classics_list_extended.json"]
    return random.choice(charts_lists_filenames)
