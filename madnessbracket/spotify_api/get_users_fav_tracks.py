from madnessbracket.spotify_api.spotify_user_oauth import check_spotify, spotify_get_users_top_tracks


def get_users_favorite_tracks():
    """
    get current user's top tracks for madness bracket
    :return: jsonified tracks dict
    """
    # check if the user's logged in and token's not expired
    user, token = check_spotify()
    if not user or not token:
        print('either user or token is none')
        return None
    # get track items from spotify
    track_items = spotify_get_users_top_tracks(token)
    if not track_items:
        print('no track items retrieved')
        return None
    # process track items filling all the needed info about the songs retrieved
    users_tracks = process_spotify_tracks(track_items)
    if not users_tracks:
        return None
    return users_tracks


def process_spotify_tracks(track_items):
    """
    process spotify's track items
    :return: a fully prepared dict with all the tracks
    """
    if not track_items:
        return None
    # initialize a dict to avoid KeyErrors
    tracks = {
        "tracks": []
    }
    # iterate through tracks
    for track in track_items:
        name = track.name
        artist_name = track.artists[0].name
        track_id = track.id
        preview_url = track.preview_url
        a_track_info = {
            "artist_name": artist_name,
            "track_title": name,
            "track_id": track_id,
            "preview_url": preview_url
        }
        tracks["tracks"].append(a_track_info)
    return tracks
