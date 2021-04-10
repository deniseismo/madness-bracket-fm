import tekore as tk
import spotipy
from fuzzywuzzy import fuzz
from madnessbracket.utilities.track_processing import get_filtered_name
from madnessbracket.utilities.fuzzymatch import fuzzy_match_song, fuzzy_match_artist
from spotipy.oauth2 import SpotifyClientCredentials
from flask import current_app
from madnessbracket.utilities.helpers import timeit


def get_spotify_spotipy_client():
    """get a spotify client via spotipy library

    Returns:
        an instance of a Spotify client
    """
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
        client_id=current_app.config['SPOTIFY_CLIENT_ID'],
        client_secret=current_app.config['SPOTIFY_CLIENT_SECRET']
    ))
    return spotify


def get_spotify_tekore_client():
    """get a spotify client via tekore library

    Returns:
        an instance of a Spotify client
    """
    client_id = current_app.config['SPOTIFY_CLIENT_ID']
    client_secret = current_app.config['SPOTIFY_CLIENT_SECRET']

    app_token = tk.request_client_token(
        client_id=client_id, client_secret=client_secret)
    spotify_tekore_client = tk.Spotify(app_token)
    return spotify_tekore_client


@timeit
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
    query = f"track:{track_title} artist:{artist_name}"
    tracks_info, = spotify_tekore_client.search(
        query=query, types=('track',), limit=15)
    # in case of not getting any response
    if not tracks_info:
        print("no tracks info")
        return None
    # special flag that is used for double-checking an artist
    # if it went through searching the track without specifying artist's name
    artist_match = True
    # in case no items found
    if tracks_info.total == 0:
        print("tracks info total 0")
        query = f"track:{track_title}"
        # try finding a song without specifying artist inside the query
        tracks_info, = spotify_tekore_client.search(
            query=query, types=('track',), limit=15)
        # change "artist match" flag to False
        artist_match = False
    if tracks_info.total == 0:
        # no tracks found whatsoever
        return None
    track_title = track_title.lower()
    matches = []
    for track in tracks_info.items:
        filtered_name = get_filtered_name(track.name).lower()
        if not artist_match:
            # double check the artist, artist's match being false means it went through search without specifying the artist's name
            # so we need to double check the artist
            artist_match = fuzzy_match_artist(
                artist_name, track.artists[0].name)
            print(artist_match)
        if filtered_name == track_title and artist_match:
            print("track found: perfect match")
            return track
        print(track.name, "→", filtered_name, "vs.", track_title,
              fuzz.ratio(filtered_name, track_title), sep=" | ")
        ratio = fuzz.ratio(filtered_name, track_title)
        if ratio > 90 and artist_match:
            print(f"pretty close: {filtered_name} vs. {track_title}")
            return track
        # append a match to matches list
        if artist_match:
            matches.append((track, ratio))
    # if there are any matches
    if matches:
        try:
            # pick with the highest ratio
            return sorted(matches, key=lambda x: x[1], reverse=True)[0][0]
        except IndexError as e:
            print(e)
            return None
    return None


def get_spotify_artist_id(artist_name: str, tekore_client=None):
    """get spotify ID for an artist (via tekore library)

    Args:
        artist_name (str): artist's name
        tekore_client (optional): an instance of a Spotify client. Defaults to None.

    Returns:
        (str): spotify ID for an artist
    """
    if not artist_name:
        return None
    # if tekore client is not provided, get a new one
    if not tekore_client:
        spotify_tekore_client = get_spotify_tekore_client()
    else:
        spotify_tekore_client = tekore_client
    query = f"{artist_name}"
    artist_info, = spotify_tekore_client.search(
        query=query, types=('artist',), limit=50, market="US")
    # in case of not getting any response
    if not artist_info:
        print("no info about the artist returned at all")
        return None
    # in case no items found
    if artist_info.total == 0:
        print(artist_info)
        print("no artists found")
        return None
    # iterate over artists found
    print(artist_info.total)
    artist_id = artist_info.items[0].id
    for index, artist in enumerate(artist_info.items):
        print(index, artist.name)
        # find the right one
        if artist.name.lower() == artist_name.lower():
            artist_id = artist.id
            return artist_id
    return artist_id


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
    artist_id = get_spotify_artist_id(
        artist_name, spotify_tekore_client)  # get ID via tekore
    if not artist_id:
        return None
    print("artist spotify id", artist_id)
    top_tracks = spotify_tekore_client.artist_top_tracks(artist_id, 'US')
    # in case of not getting any response
    if not top_tracks:
        return None
    return top_tracks


def spotipy_get_artist_id(artist_name: str):
    """search for an artist's id (via spotipy library)
    TODO: non-latin artist's names

    Args:
        artist_name (str): artist's name

    Returns:
        (str): spotify's artist's ID
    """
    spotify = get_spotify_spotipy_client()
    try:
        artist_info = spotify.search(
            q=artist_name, type="artist", limit=5, market='US')
    except spotipy.exceptions.SpotifyException:
        return None
    if not artist_info:
        return None
    artist_id = None
    print(artist_info['artists']['items'])
    for item in artist_info['artists']['items']:
        print(item['name'].lower(), artist_name.lower())
        if item['name'].lower() == artist_name.lower():
            try:
                print('artists name are equal!')
                artist_id = item['id']
                break
            except KeyError:
                return None
    return artist_id


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
    album_spotify_id = get_spotify_album_id(
        album_title, artist_name, tekore_client)
    if not album_spotify_id:
        return None
    album_tracks = spotify_tekore_client.album_tracks(
        album_spotify_id, limit=50)
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


def get_spotify_album_id(album_title, artist_name, tekore_client=None):
    """gets album's spotify ID

    Args:
        album_title (str): album's title
        artist_name (str): artist's name
        tekore_client (optional): an instance of a Spotify client. Defaults to None.

    Returns:
        (str): album's spotify ID
    """
    if not artist_name or not album_title:
        return None
    # if tekore client is not provided, get a new one
    if not tekore_client:
        spotify_tekore_client = get_spotify_tekore_client()
    else:
        spotify_tekore_client = tekore_client

    query = f"{album_title}"
    albums_found, = spotify_tekore_client.search(
        query=query, types=('album',), limit=50)
    print(albums_found)
    # in case of not getting any response
    if not albums_found:
        print("no info about the artist returned at all")
        return None
    # in case no items found
    if albums_found.total == 0:
        print(albums_found)
        print("no artists found")
        return None
    # iterate over artists found
    print(albums_found.total)
    for index, album in enumerate(albums_found.items):
        print(index, album.name)
        print(album.artists[0].name)
        # find the right one
        album_found_artist_name = album.artists[0].name
        if album_found_artist_name.lower() == artist_name.lower():
            return album.id
    return None
