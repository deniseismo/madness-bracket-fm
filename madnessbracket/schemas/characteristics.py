from typing import NamedTuple


class TrackIdentity(NamedTuple):
    """
    namedtuple used to store track's 'identity': artist's name & title combination;
    used to filter out duplicates when processing lists of tracks found on spotify, lastfm, etc.

    :attr title: (str) track's title
    :attr artist_name: (str) artist's name
    """
    title: str
    artist_name: str
