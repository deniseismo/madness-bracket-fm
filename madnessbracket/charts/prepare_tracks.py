import random
from madnessbracket.utilities.bracket_sizing import get_capped_bracket_size


def prepare_tracks_for_charts(tracks: list, limit=16) -> list:
    """
    randomizes & caps (at a given limit, default=32) tracks/songs
    :param limit: maximum number of tracks in a bracket
    :param tracks: a tracks dict with the list of 'track info' dicts
    :return: randomized & capped tracks
    """
    number_of_tracks = len(tracks)
    print('total amount of tracks: ', number_of_tracks)
    tracks_cap = get_capped_bracket_size(number_of_tracks, limit)
    random.shuffle(tracks)
    tracks = tracks[:tracks_cap]
    return tracks
