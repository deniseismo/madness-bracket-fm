from typing import Optional

from madnessbracket.schemas.track_schema import TrackInfo
from madnessbracket.track_processing.track_processing_helpers import sort_artist_tracks, \
    get_weighted_random_selection_of_tracks, add_text_color_to_tracks
from madnessbracket.utilities.bracket_sizing import get_capped_bracket_size


def prepare_tracks(tracks: list[TrackInfo], limit: int = 16) -> list[TrackInfo]:
    """
    randomizes & caps (at a given limit, default=32) tracks/songs
    :param limit: maximum number of tracks in a bracket
    :param tracks: a tracks dict with the list of 'track info' dicts
    :return: randomized & capped tracks
    """
    number_of_tracks = len(tracks)
    tracks_cap = get_capped_bracket_size(number_of_tracks, limit)
    sort_artist_tracks(tracks)
    tracks = tracks[:tracks_cap]
    return tracks


def prepare_tracks_for_artist_battle(
        artist_1_tracks: list[TrackInfo],
        artist_2_tracks: list[TrackInfo],
        bracket_size: int
) -> list[TrackInfo]:
    """
    prepare (cap & randomize) tracks for the battle of artists
    :param artist_1_tracks: (list[TrackInfo]) tracks by artist 1
    :param artist_2_tracks: (list[TrackInfo]) tracks by artist 2
    :param bracket_size: (int) chosen bracket size
    :return: (list[TrackInfo]) a list of zipped tracks by two artists chosen to battle each other
    """
    min_number_of_tracks = min([len(artist_1_tracks), len(artist_2_tracks)])
    tracks_cap = get_capped_bracket_size(min_number_of_tracks, bracket_size)
    song_count_per_artist = int(tracks_cap / 2)
    sort_artist_tracks(artist_1_tracks)
    sort_artist_tracks(artist_2_tracks)
    artist_1_tracks_processed = artist_1_tracks[:song_count_per_artist]
    artist_2_tracks_processed = artist_2_tracks[:song_count_per_artist]
    battle_tracks = []
    for (track_a, track_b) in zip(artist_1_tracks_processed, artist_2_tracks_processed):
        battle_tracks.append(track_a)
        battle_tracks.append(track_b)
    add_text_color_to_tracks(battle_tracks)
    return battle_tracks


def prepare_tracks_for_artist(tracks: list[TrackInfo], limit: int = 16) -> Optional[list[TrackInfo]]:
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
    tracks_cap = get_capped_bracket_size(number_of_tracks, limit)
    randomized_tracks = get_weighted_random_selection_of_tracks(tracks, tracks_cap)
    if not randomized_tracks:
        return None
    add_text_color_to_tracks(randomized_tracks)
    return randomized_tracks
