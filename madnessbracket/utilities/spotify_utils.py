import random


def prepare_tracks(tracks: dict):
    """
    randomizes & caps (at 32) tracks/songs
    :param tracks: a tracks dict with the list of 'track info' dicts
    :return:
    """
    MAX_TRACKS = 32
    # shuffles tracks
    random.shuffle(tracks['tracks'])
    # make sure it's divisible by 4 (madness bracket structure rule)
    tracks_len = len(tracks['tracks']) // 4 * 4
    # caps at 32 max or a lesser dividend
    tracks_cap = min(32, tracks_len)
    tracks['tracks'] = tracks['tracks'][:tracks_cap]
    return tracks
