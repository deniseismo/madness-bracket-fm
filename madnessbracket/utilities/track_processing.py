import random
import re
from madnessbracket.utilities.randomize_track_selection import get_weighted_random_selection_of_tracks


def cap_tracks(tracks: dict, limit: int = 16):
    """
    randomizes & caps (at a given limit, default=32) tracks/songs
    :param limit: maximum number of tracks in a bracket
    :param tracks: a tracks dict with the list of 'track info' dicts
    :return: randomized & capped tracks
    """
    # standard measurements of the bracket: 4, 8, 16, or 32 tracks
    bracket_standards = [4, 8, 16, 32]
    # capping the standards with the limit given
    capped_standards = list(filter(lambda x: x <= limit, bracket_standards))
    # get the total amount of tracks
    number_of_tracks = len(tracks['tracks'])
    print('total amount of tracks: ', number_of_tracks)
    # figure out what the tracks cap should be: the closest maximum number out of the bracket standards
    tracks_cap = max(list(filter(lambda x: x <= number_of_tracks, capped_standards)))
    randomized_tracks = get_weighted_random_selection_of_tracks(tracks['tracks'], tracks_cap)
    return randomized_tracks


def get_filtered_name(name_to_fix: str):
    """
    :param name_to_fix: a song name to fix
    :return: a filtered name
    """
    # replace some weird characters with normal ones
    a_correct_title = fix_quot_marks(name_to_fix)
    patterns = [
        # no special words in brackets
        r"\(.*((\bremaster)|(\banniversary)|(\bEdition)|(\bmix)|(\bdeluxe)|(\bCD)|(\bsoundtrack)|(\bComplete)|(\bRemix)).*\)",
        r"(\-\s\w+\s(remix)\s?.*)",
        r"((super)?\s?(deluxe)\s?).*",
        r"(\-?\s?(\d+)?\s?(stereo|digital)?\s?(Remaster|acoustic)\s?).*",
        r"((recorded)? live at .*)",
        r"((\d+)?\s?(Bonus Tracks)\s?).*",
        r"((\d+)?\s?(International Version)\s?).*",
        r"\d+?(th)?\s?Anniversary\s?\w*",
        r"(\s(\d+)?\s?(remix)\s?).*",
        r"((-\s.+)?\s(\d+)?\s?(original)?\s?(album|mono|stereo)?\s?(mix|version)).*",
        r"(- Live)",
        r"(- .*edit)",
        r"(b-side)",
        r"((BBC)\s(.*)\s(session).*)",
        r"((MTV)\s.*)",
        r"(\(from\s.*\))",
        # no weird characters
        r"[“”:\(\)\":…]",
    ]
    for pattern in patterns:
        a_correct_title = re.sub(
            pattern, '', a_correct_title, flags=re.IGNORECASE)
    # finally remove some trailing hyphens and/or whitespaces
    ultimate_filtered_name = a_correct_title.strip('- ')
    return ultimate_filtered_name


def fix_quot_marks(song_name):
    """
    fixes (’,“, ”)
    """
    song_name = song_name.replace("’", "'").replace(
        "‘", "'").replace('“', '"').replace('”', '"')
    return song_name


def remove_quot_marks_on_both_sides(string_to_fix):
    """removes quotation marks if they are present on both sides of the string only
    e.g. Die Frau ohne Schatten: III. Aufzug. "Wenn das Herz aus Kristall zerbricht in einem Schrei" → nope
    e.g. "Heroes" → yep
    """
    if not string_to_fix:
        return None
    pattern = r'(^[\"\'].*[\"\']$)'
    match = re.findall(pattern, string_to_fix)
    if match:
        string_to_fix = string_to_fix.strip('"\'')
    return string_to_fix
