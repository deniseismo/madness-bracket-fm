from fuzzywuzzy import fuzz

from madnessbracket.music_apis.spotify_api.spotify_artist_handlers import get_spotify_artist_info
from madnessbracket.music_apis.spotify_api.spotify_client_api import get_spotify_tekore_client
from madnessbracket.utilities.fuzzymatch import fuzzy_match_artist
from madnessbracket.utilities.name_filtering import get_filtered_name


def get_spotify_albums_tracks(album_title: str, artist_name: str, tekore_client=None):
    """get particular album's tracks

    Args:
        album_title (str): album's title
        artist_name (str): artist's name
        tekore_client (optional): an instance of a Spotify client. Defaults to None.

    Returns:
        (List): a list of album's tracks
    """
    # if tekore client is not provided, get a new one
    if not tekore_client:
        spotify_tekore_client = get_spotify_tekore_client()
    else:
        spotify_tekore_client = tekore_client
    # get album's id on spotify
    album_spotify_info = get_spotify_album_info(
        album_title, artist_name, tekore_client)
    if not album_spotify_info:
        return None
    album_tracks = spotify_tekore_client.album_tracks(
        album_spotify_info.id, limit=50)
    print(album_tracks)
    if not album_tracks:
        print("nothing found")
        return None
    if album_tracks.total == 0:
        print("no tracks found")
        return None
    for track in album_tracks.items:
        print(track)
        print(dir(track))
    return album_tracks.items


def get_spotify_album_info(album_title, artist_name, tekore_client=None):
    """search for an album → get album info (simplified)

    Args:
        album_title (str): album's title
        artist_name (str): artist's name
        tekore_client (optional): an instance of a Spotify client. Defaults to None.

    Returns:
        (tekore.SimpleAlbum): tekore.SimpleAlbum (album info object, NO info about TRACKS inside)
    """
    if not artist_name or not album_title:
        return None
    # if tekore client is not provided, get a new one
    if not tekore_client:
        spotify_tekore_client = get_spotify_tekore_client()
    else:
        spotify_tekore_client = tekore_client
    albums_found = get_album_search_results(
        album_title, artist_name, spotify_tekore_client)
    if not albums_found:
        return None
    artist_spotify_info = get_spotify_artist_info(
        artist_name, spotify_tekore_client)
    spotify_artist_name = artist_spotify_info.name if artist_spotify_info else None
    perfect_match = find_album_best_match(
        album_title, artist_name, spotify_artist_name, albums_found.items)
    if not perfect_match:
        return None
    return perfect_match


def get_album_search_results(album_title: str, artist_name: str, spotify_tekore_client):
    """
    search for a particular album on spotify
    :param album_title: album's title
    :param artist_name: artist's name
    :param spotify_tekore_client: an instance of a Spotify client. Defaults to None.
    :return: all the albums found (max=50)
    """
    query = f"{album_title} artist:{artist_name}"
    albums_found, = spotify_tekore_client.search(
        query=query, types=('album',), limit=50)
    # in case of not getting any response
    if not albums_found:
        print("search for album failed")
        return None
    # in case no items found
    if albums_found.total == 0:
        print("no albums found (with artist specified)")
        query = f"{album_title}"
        # try finding a song without specifying artist inside the query
        albums_found, = spotify_tekore_client.search(
            query=query, types=('album',), limit=50)
        # change "artist match" flag to False
    if albums_found.total == 0:
        # no tracks found whatsoever
        return None
    return albums_found


def find_album_best_match(album_title: str, artist_name: str, spotify_artist_name: str, search_results: list):
    """find the most appropriate (best) match amongst all the search results for an album to find

    :param album_title: track's title to find
    :param artist_name: artist's name
    :param spotify_artist_name: artist's name on Spotify
    :param search_results: a list of all the search results
    :return: perfect match if found
    """
    print(
        f"searching for Album({album_title}) among {len(search_results)} results")
    matches = []
    for album in search_results:
        album_found = get_filtered_name(album.name).lower()
        if spotify_artist_name and spotify_artist_name != artist_name:
            correct_artist_found = fuzzy_match_artist(
                artist_name, album.artists[0].name) or fuzzy_match_artist(
                spotify_artist_name, album.artists[0].name)
        else:
            correct_artist_found = fuzzy_match_artist(
                artist_name, album.artists[0].name)
        print(correct_artist_found)
        if not correct_artist_found:
            print("INCORRECT ARTIST")
            continue
        if album_found == album_title:
            print("album found: perfect match")
            return album
        print(album.name, "→", album_found, "vs.", album_title,
              fuzz.ratio(album_found, album_title), sep=" | ")
        ratio = fuzz.ratio(album_found, album_title)
        if ratio > 90:
            print(f"pretty close: {album_found} vs. {album_title}")
            return album
        if ratio > 80:
            # append a match to matches list
            matches.append((album, ratio))
    # if there are matches
    if matches:
        try:
            # pick track with the highest ratio
            return sorted(matches, key=lambda x: x[1], reverse=True)[0][0]
        except IndexError as e:
            print(e)
            return None
    return None
