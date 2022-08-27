from madnessbracket.music_apis.spotify_api.spotify_async_artist_handlers import fetch_spotify_artist_info
from madnessbracket.music_apis.spotify_api.spotify_client_api import get_spotify_tekore_client
from madnessbracket.music_apis.spotify_api.spotify_track_handlers import find_track_best_match


async def fetch_spotify_track_info(track_title: str, artist_name: str, tekore_client=None):
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
    tracks_found = await fetch_track_search_results(
        track_title, artist_name, spotify_tekore_client)
    if not tracks_found:
        return None
    artist_spotify_info = await fetch_spotify_artist_info(
        artist_name, spotify_tekore_client)
    spotify_artist_name = artist_spotify_info.name if artist_spotify_info else None
    perfect_match = find_track_best_match(
        track_title, artist_name, spotify_artist_name, tracks_found.items)
    if not perfect_match:
        return None
    return perfect_match


async def fetch_track_search_results(track_title: str, artist_name: str, spotify_tekore_client):
    """
    search for a particular track on spotify
    :param track_title: song's title
    :param artist_name: artist's name
    :param spotify_tekore_client: an instance of a Spotify client. Defaults to None.
    :return: all the tracks found (max=15)
    """
    query = f"{track_title} artist:{artist_name}"
    tracks_found, = await spotify_tekore_client.search(
        query=query, types=('track',), limit=15, market="GE")
    # in case of not getting any response
    if not tracks_found:
        print("search for track failed")
        return None
    # in case no items found
    if tracks_found.total == 0:
        print("no tracks found (with artist specified)")
        query = f"{track_title}"
        # try finding a song without specifying artist inside the query
        tracks_found, = await spotify_tekore_client.search(
            query=query, types=('track',), limit=15)
        # change "artist match" flag to False
    if tracks_found.total == 0:
        # no tracks found whatsoever
        return None
    return tracks_found
