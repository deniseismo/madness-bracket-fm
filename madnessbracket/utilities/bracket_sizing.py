def get_capped_bracket_size(number_of_tracks: int, chosen_upper_limit: int):
    """
    cap the bracket size at a maximum appropriate bracket size possible,
        that is within [4, 8, 16, 32] but <= upper limit
    :param number_of_tracks:
    :param chosen_upper_limit:
    :return: capped bracket size
    """
    if not number_of_tracks:
        return None
    if number_of_tracks < 4:
        return None
    # standard measurements of the bracket: 4, 8, 16, or 32 tracks
    bracket_standards = [4, 8, 16, 32]
    # capping the standards with the limit given
    capped_standards = list(
        filter(lambda x: x <= chosen_upper_limit, bracket_standards))
    # figure out what the tracks cap should be: the closest maximum number out of the bracket standards
    tracks_cap = max(
        list(filter(lambda x: x <= number_of_tracks, capped_standards)))
    return tracks_cap
