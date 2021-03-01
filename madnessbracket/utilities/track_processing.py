import random
import re


def cap_tracks(tracks: dict, limit: int = 32):
    """
    randomizes & caps (at a given limit, default=32) tracks/songs
    :param tracks: a tracks dict with the list of 'track info' dicts
    :return:
    """
    # shuffles tracks
    random.shuffle(tracks['tracks'])
    # make sure it's divisible by 4 (madness bracket structure rule)
    tracks_len = len(tracks['tracks']) // 4 * 4
    # caps at 32 max or a lesser dividend
    tracks_cap = min(limit, tracks_len)
    tracks['tracks'] = tracks['tracks'][:tracks_cap]
    return tracks


def get_filtered_name(name_to_fix: str):
    """
    :param name_to_fix: a song name to fix
    :return: a fitlered name
    """
    # TODO: (mono/stereo) &/and
    # replace some weird characters with normal ones
    a_correct_title = name_to_fix.replace("’", "'")
    patterns = [
        # no special words in brackets
        r"\(.*((\bremaster)|(\banniversary)|(\bEdition)|(\bmix)|(\bdeluxe)|(\bCD)|(\bsoundtrack)|(\bComplete)).*\)|\[.*\]",
        # no super deluxe
        r"((super)?\s?(deluxe)\s?).*",
        r"(\-?\s?(\d+)?\s?(Remaster)\s?).*",
        r"((\d+)?\s?(Bonus Tracks)\s?).*",
        r"((\d+)?\s?(International Version)\s?).*",
        r"\d+?(th)?\s?Anniversary\s?\w*",
        r"(\s(\d+)?\s?(remix)\s?).*",
        # no weird characters
        r"[“”:\(\)\":…]"
    ]
    for pattern in patterns:
        a_correct_title = re.sub(
            pattern, '', a_correct_title, flags=re.IGNORECASE)
    # finally remove some trailing hyphens and/or whitespaces
    ultimate_filtered_name = a_correct_title.strip('-').strip()
    return ultimate_filtered_name


def fix_quot_marks(song_name):
    """
    fixes (’,“, ”)
    """
    song_name = song_name.replace("’", "'").replace('“', '"').replace('”', '"')
    return song_name
