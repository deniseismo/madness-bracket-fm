import json
import math
import random
from typing import Optional

from madnessbracket import cache
from madnessbracket.schemas.response import TracksInfoResponse
from madnessbracket.schemas.track_schema import TrackInfo
from madnessbracket.utilities.color_processing import get_contrast_color_for_two_color_gradient


def make_tracks_info_response(
        tracks: list[TrackInfo],
        description: str,
        value1: str = None,
        value2: str = None,
        extra: str = None
) -> TracksInfoResponse:
    """
    make a TracksInfoResponse (ready to be jsonified and sent to the user)
    :param tracks: (list[TrackInfo]) list of processed tracks (TrackInfo)
    :param description: (str) madness bracket description info (name/title for the bracket)
    :param value1: (str) 'main name' (e.g. artist's name, username, etc.)
    :param value2: (str) secondary name (e.g. second artist's name for the artists battle)
    :param extra: (str) extra info about the bracket type (e.g. battle, secret)
    :return: (TrackInfoResponse)
    """
    tracks_info_response = TracksInfoResponse(
        tracks=tracks,
        description=description
    )
    if value1:
        tracks_info_response.value1 = value1
    if value2:
        tracks_info_response.value2 = value2
    if extra:
        tracks_info_response.extra = extra
    return tracks_info_response


def sort_artist_tracks(tracks: list[TrackInfo]) -> None:
    """
    sort artist tracks randomly
    :param tracks: (list[TrackInfo])
    """
    random.seed()
    random.shuffle(tracks)
    return None


def get_weighted_random_selection_of_tracks(tracks: list[TrackInfo], bracket_size: int) -> Optional[list[TrackInfo]]:
    """
    :param tracks:
    :param bracket_size:
    :return:
    """
    if not tracks or not bracket_size:
        return None
    # get the total number of tracks
    tracks_to_choose_from = list(tracks)
    length = len(tracks)
    # calculate portions we need tracks to divide into: top 1-30%, 31-75%, bottom 25%
    portions = [math.floor(x) for x in [0.3 * length, 0.45 * length]]
    portions.append(length - sum(portions))
    # give those portions weight: e.g. the first portion (top 1-30%) would be selected 6 out of 11 times,
    # the second one — 4/11, etc.
    weight_ratios = [10, 4, 2]
    portions_and_ratios = zip(portions, weight_ratios)
    # populate weights list
    weights = []
    for (size, weight) in portions_and_ratios:
        weights += [weight for _ in range(size)]
    # get weighted random tracks
    selected_tracks = []
    for _ in range(bracket_size):
        choice = random.choices(tracks_to_choose_from, weights=weights)[0]
        selected_tracks.append(choice)
        # remove track from the list so it doesn't come up twice
        choice_index = tracks_to_choose_from.index(choice)
        tracks_to_choose_from.pop(choice_index)
        # fix weights list as well, as it has to be of the same size as the list of tracks to choose from
        weights.pop(choice_index)
    return selected_tracks


def add_text_color_to_tracks(tracks: list[TrackInfo]) -> None:
    """
    dynamically add the most appropriate contrast text color,
    so that text's readable  (where applicable)
    :param tracks: a list of dicts with all the needed info about songs/tracks
    :return:
    """
    if not tracks:
        return None
    for track in tracks:
        if not track.album_colors:
            continue
        try:
            dominant_color = track.album_colors[0]
            secondary_color = track.album_colors[1]
            text_color = get_contrast_color_for_two_color_gradient(dominant_color, secondary_color)
            track.text_color = text_color
        except (ValueError, IndexError) as e:
            print(e)


@cache.memoize(timeout=36000)
def load_tracks_from_file(filepath) -> Optional[list[dict[str]]]:
    """load tracks from json file

    Returns:
        [list]: of songs
    """
    try:
        with open(filepath, encoding='utf-8') as f:
            tracks = json.load(f)
    except IOError as e:
        print('file not found', e)
        return None
    return tracks