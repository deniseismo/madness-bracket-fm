import random

import tekore as tk

from madnessbracket.musician.prepare_tracks import add_text_color_to_tracks
from madnessbracket.profile.spotify.spotify_profile_oauth import spotify_tekore_client
from madnessbracket.profile.spotify.prepare_tracks import prepare_spotify_tracks


def get_spotify_bracket_data(token, bracket_limit):
    """
    a shortcut function that combines all the other spotify handlers
    :param token: user's Spotify (tekore lib) token
    :param bracket_limit: chosen bracket upper limit
    :return: a dict with all the musician bracket data
    """
    username, user_tracks = spotify_get_users_top_tracks(token)
    if not user_tracks:
        return None
    user_tracks = prepare_spotify_tracks(user_tracks, bracket_limit)
    add_text_color_to_tracks(user_tracks)
    tracks = {
        "tracks": user_tracks,
        "description": f"{username}: My Spotify",
        "extra": None
    }
    return tracks


def spotify_get_users_top_tracks(token):
    """get current user top tracks (items)
    :return: current user's top track items

    Args:
        token: access token

    Returns:
        current user's top track items
    """
    # spotify's internal 'time spans': gives different selections of your fav. tracks based on time period
    time_periods = ['short_term', 'medium_term', 'long_term']
    if not token:
        return None
    try:
        with spotify_tekore_client.token_as(token):
            current_user = spotify_tekore_client.current_user()
            username = current_user.display_name
            # get user's top 50 tracks (pick time span at random)
            top_tracks = spotify_tekore_client.current_user_top_tracks(
                limit=50, time_range=random.choice(time_periods))
    except tk.HTTPError:
        return None

    if not top_tracks:
        return None

    if not top_tracks.items:
        return None
    print(top_tracks.total)
    if len(top_tracks.items) < 4:
        print('not enought tracks')
        return None
    return username, top_tracks.items
