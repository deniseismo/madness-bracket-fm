from madnessbracket.music_apis.spotify_api.spotify_artist_handlers import find_artist_best_match
from madnessbracket.music_apis.spotify_api.spotify_client_api import get_spotify_tekore_client


async def fetch_spotify_artist_info(artist_name: str, tekore_client=None):
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
    artists_found = await fetch_artist_id_search_results(
        artist_name, spotify_tekore_client)
    if not artists_found:
        return None
    perfect_match = find_artist_best_match(artist_name, artists_found.items)
    if not perfect_match:
        return None
    return perfect_match


async def fetch_artist_id_search_results(artist_name: str, spotify_tekore_client):
    """
    search for a particular artist on spotify
    :param artist_name: artist's name
    :param spotify_tekore_client: an instance of a Spotify client. Defaults to None.
    :return: artists found (max=15)
    """
    query = f"{artist_name}"
    artists_found, = await spotify_tekore_client.search(
        query=query, types=('artist',), market="GE", limit=50)
    # in case of not getting any response
    if not artists_found:
        print("search for track failed")
        return None
    if artists_found.total == 0:
        # no tracks found whatsoever
        return None
    return artists_found
