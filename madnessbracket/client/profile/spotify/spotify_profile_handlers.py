from typing import Optional

from madnessbracket.music_apis.spotify_api.spotify_user_handlers import spotify_get_users_top_tracks
from madnessbracket.schemas.spotify_user_info import SpotifyTopTracksProcessedInfo
from madnessbracket.track_processing.track_preparation import prepare_tracks
from madnessbracket.track_processing.track_processing_helpers import add_text_color_to_tracks


def get_tracks_for_spotify_user(token, bracket_limit: int) -> Optional[SpotifyTopTracksProcessedInfo]:
    """
    get spotify top tracks processed info with spotify user's username & processed tracks
    :param token: user's access token
    :param bracket_limit: (int) bracket upper limit
    :return: (SpotifyTopTracksProcessedInfo) with username & processed tracks ready for madness bracket
    """
    spotify_top_tracks_info = spotify_get_users_top_tracks(token)
    if not spotify_top_tracks_info:
        return None
    spotify_top_tracks_info.tracks = prepare_tracks(spotify_top_tracks_info.tracks, bracket_limit)
    add_text_color_to_tracks(spotify_top_tracks_info.tracks)
    return spotify_top_tracks_info
