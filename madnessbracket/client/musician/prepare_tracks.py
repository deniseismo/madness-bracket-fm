from typing import Optional

from madnessbracket.schemas.track_schema import TrackInfo
from madnessbracket.track_processing.track_randomization import get_weighted_random_selection_of_tracks
from madnessbracket.utilities.bracket_sizing import get_capped_bracket_size
from madnessbracket.utilities.color_processing import get_contrast_color_for_two_color_gradient


def prepare_tracks_for_musician(tracks: list, limit=16) -> Optional[list]:
    """
    randomizes & caps (at a given limit, default=32) tracks/songs;
    uses weighted random selection for better sorting/randomization
    :param limit: maximum number of tracks in a bracket
    :param tracks: a list of tracks
    :return: randomized & capped tracks
    """
    if not tracks:
        return None
    number_of_tracks = len(tracks)
    print('total amount of tracks: ', number_of_tracks)
    tracks_cap = get_capped_bracket_size(number_of_tracks, limit)
    randomized_tracks = get_weighted_random_selection_of_tracks(
        tracks, tracks_cap)
    if not randomized_tracks:
        return None
    add_text_color_to_tracks(randomized_tracks)
    return randomized_tracks


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
            text_color = get_contrast_color_for_two_color_gradient(
                dominant_color, secondary_color)
            track.text_color = text_color
        except (ValueError, IndexError) as e:
            print(e)


