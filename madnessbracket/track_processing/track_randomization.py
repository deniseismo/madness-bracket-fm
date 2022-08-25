import math
import random
from typing import Optional


def get_weighted_random_selection_of_tracks(tracks: list, bracket_size: int) -> Optional[list]:
    """[summary]

    Args:
        tracks (list): a list of all the tracks to choose from
        bracket_size (int): bracket size (number of tracks needed)

    Returns:
        (list): list of weighted random tracks
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
