import re


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
        r"\(live\s?(version)?\)",
        r"(- Studio)",
        r"(- .*edit)",
        r"(b-side)",
        r"((BBC)\s(.*)\s(session).*)",
        r"((from)\s(.*)\s(soundtrack))",
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


def fix_quot_marks(song_name: str):
    """
    fixes (’,“, ”)
    """
    song_name = song_name.replace("’", "'").replace(
        "‘", "'").replace('“', '"').replace('”', '"')
    return song_name


def fix_hyphen(string_to_fix: str):
    """replaces weird hyphen sign (often found on MusicBrainz) with the normal one (hyphen-minus)

    Args:
        string_to_fix (str): fixed string
    """
    return string_to_fix.replace("‐", "-")


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
