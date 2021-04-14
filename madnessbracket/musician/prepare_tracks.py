from madnessbracket.utilities.randomize_track_selection import get_weighted_random_selection_of_tracks
from madnessbracket.utilities.track_processing import get_capped_bracket_size


def prepare_tracks_for_musician(tracks: dict, limit=16):
    """
    randomizes & caps (at a given limit, default=32) tracks/songs;
    uses weighted random selection for better sorting/randomization
    :param limit: maximum number of tracks in a bracket
    :param tracks: a tracks dict with the list of 'track info' dicts
    :return: randomized & capped tracks
    """
    number_of_tracks = len(tracks['tracks'])
    print('total amount of tracks: ', number_of_tracks)
    tracks_cap = get_capped_bracket_size(number_of_tracks, limit)
    randomized_tracks = get_weighted_random_selection_of_tracks(
        tracks['tracks'], tracks_cap)
    tracks['tracks'] = randomized_tracks
    return tracks
