from fuzzywuzzy import fuzz

from madnessbracket import cache
from madnessbracket.dev.spotify.spotify_client_api import get_spotify_tekore_client


@cache.memoize(timeout=3600)
def get_spotify_artist_info(artist_name: str, tekore_client=None):
    """get spotify ID for an artist (via tekore library)

    Args:
        artist_name (str): artist's name
        tekore_client (optional): an instance of a Spotify client. Defaults to None.

    Returns:
        (tekore.FullArtist): tekore.FullArtist (Artist info object)
    """
    if not artist_name:
        return None
    # if tekore client is not provided, get a new one
    if not tekore_client:
        spotify_tekore_client = get_spotify_tekore_client()
    else:
        spotify_tekore_client = tekore_client
    artists_found = get_artist_id_search_results(
        artist_name, spotify_tekore_client)
    if not artists_found:
        return None
    perfect_match = find_artist_best_match(artist_name, artists_found.items)
    if not perfect_match:
        return None
    return perfect_match


def get_artist_id_search_results(artist_name: str, spotify_tekore_client):
    """
    search for a particular artist on spotify
    :param artist_name: artist's name
    :param spotify_tekore_client: an instance of a Spotify client. Defaults to None.
    :return: artists found (max=15)
    """
    query = f"{artist_name}"
    artists_found, = spotify_tekore_client.search(
        query=query, types=('artist',), market="GE", limit=50)
    # in case of not getting any response
    if not artists_found:
        print("search for track failed")
        return None
    if artists_found.total == 0:
        # no tracks found whatsoever
        return None
    return artists_found


def find_artist_best_match(artist_name: str, search_results: list):
    """find the most appropriate (best) match amongst all the search results for an artist id to find

    :param artist_name: artist's name
    :param search_results: a list of all the search results
    :return: perfect match if found
    """
    print(
        f"searching for Artist({artist_name}) among {len(search_results)} results")
    print([result.name for result in search_results])
    first_result = search_results[0]
    print(f"first result: {first_result}")
    artist_name = artist_name.lower()
    if not artist_name.isascii():
        print('non-latin artist name')
        return first_result
    matches = []
    for index, artist in enumerate(search_results):
        print(index, artist.name)
        # find the right one
        if artist.name.lower() == artist_name:
            return artist
        ratio = fuzz.ratio(artist.name.lower(), artist_name)
        print(ratio)
        if ratio > 95:
            print(f"pretty close: {artist.name} vs. {artist_name}")
            return artist
        if ratio > 90:
            matches.append((artist, ratio))
    if matches:
        try:
            # pick with the highest ratio
            return sorted(matches, key=lambda x: x[1], reverse=True)[0][0]
        except IndexError as e:
            print(e)
            return None
    return first_result


def get_spotify_artist_top_tracks(artist_name: str, tekore_client=None):
    """get artist's top tracks according to spotify
    Args:
        artist_name (str): [description]
        tekore_client ([type], optional): [description]. Defaults to None.

    Returns:
        (tekore.ListObject): a list-like object with all the top tracks and their info
    """
    if not artist_name:
        return None
    # if tekore client is not provided, get a new one
    if not tekore_client:
        spotify_tekore_client = get_spotify_tekore_client()
    else:
        spotify_tekore_client = tekore_client
    artist_info = get_spotify_artist_info(
        artist_name, spotify_tekore_client)  # get ID via tekore
    if not artist_info:
        return None
    print("artist spotify id", artist_info.id)
    top_tracks = spotify_tekore_client.artist_top_tracks(artist_info.id, 'GE')
    # in case of not getting any response
    if not top_tracks:
        return None
    return top_tracks
