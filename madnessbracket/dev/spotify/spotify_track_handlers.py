from fuzzywuzzy import fuzz

from madnessbracket import cache
from madnessbracket.dev.spotify.spotify_artist_handlers import get_spotify_artist_info
from madnessbracket.dev.spotify.spotify_client_api import get_spotify_tekore_client
from madnessbracket.utilities.fuzzymatch import fuzzy_match_artist
from madnessbracket.utilities.track_filtering import get_filtered_name


@cache.memoize(timeout=3600)
def get_spotify_track_info(track_title: str, artist_name: str, tekore_client=None):
    """search for a track → get track info
    Args:
        track_title (str): track's title
        artist_name (str): artist's name
        tekore_client (optional): an instance of a Spotify client. Defaults to None.

    Returns:
        (tekore.FullTrack): tekore.FullTrack (track info object)
    """
    if not track_title or not artist_name:
        return None
    # if tekore client is not provided, get a new one
    if not tekore_client:
        spotify_tekore_client = get_spotify_tekore_client()
    else:
        spotify_tekore_client = tekore_client
    tracks_found = get_track_search_results(
        track_title, artist_name, spotify_tekore_client)
    if not tracks_found:
        return None
    perfect_match = find_track_best_match(
        track_title, artist_name, tracks_found.items, spotify_tekore_client)
    if not perfect_match:
        return None
    return perfect_match


def get_track_search_results(track_title: str, artist_name: str, spotify_tekore_client):
    """
    search for a particular track on spotify
    :param track_title: song's title
    :param artist_name: artist's name
    :param spotify_tekore_client: an instance of a Spotify client. Defaults to None.
    :return: all the tracks found (max=15)
    """
    query = f"{track_title} artist:{artist_name}"
    tracks_found, = spotify_tekore_client.search(
        query=query, types=('track',), limit=15)
    # in case of not getting any response
    if not tracks_found:
        print("search for track failed")
        return None
    # in case no items found
    if tracks_found.total == 0:
        print("no tracks found (with artist specified)")
        query = f"{track_title}"
        # try finding a song without specifying artist inside the query
        tracks_found, = spotify_tekore_client.search(
            query=query, types=('track',), limit=15)
        # change "artist match" flag to False
    if tracks_found.total == 0:
        # no tracks found whatsoever
        return None
    return tracks_found


def find_track_best_match(track_title: str, artist_name: str, search_results: list, spotify_tekore_client):
    """find the most appropriate (best) match amongst all the search results for a track to find

    :param spotify_tekore_client: an instance of a Spotify tekore client
    :param track_title: track's title to find
    :param artist_name: artist's name
    :param search_results: a list of all the search results
    :return: perfect match if found
    """
    track_title = track_title.lower()
    artist_spotify_info = get_spotify_artist_info(
        artist_name, spotify_tekore_client)
    spotify_artist_name = artist_spotify_info.name if artist_spotify_info else None
    matches = []
    for track in search_results:
        track_found = get_filtered_name(track.name).lower()
        if spotify_artist_name and spotify_artist_name != artist_name:
            correct_artist_found = fuzzy_match_artist(
                artist_name, track.artists[0].name) or fuzzy_match_artist(
                spotify_artist_name, track.artists[0].name)
        else:
            correct_artist_found = fuzzy_match_artist(
                artist_name, track.artists[0].name)
        print(correct_artist_found)
        if not correct_artist_found:
            print("INCORRECT ARTIST")
            continue
        if track_found == track_title:
            print("track found: perfect match")
            return track
        print(track.name, "→", track_found, "vs.", track_title,
              fuzz.ratio(track_found, track_title), sep=" | ")
        ratio = fuzz.ratio(track_found, track_title)
        if ratio > 90:
            print(f"pretty close: {track_found} vs. {track_title}")
            return track
        # append a match to matches list
        matches.append((track, ratio))
    # if there are matches
    if matches:
        try:
            # pick track with the highest ratio
            return sorted(matches, key=lambda x: x[1], reverse=True)[0][0]
        except IndexError as e:
            print(e)
            return None
    return None
