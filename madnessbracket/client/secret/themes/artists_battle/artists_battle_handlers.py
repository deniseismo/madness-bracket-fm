from madnessbracket.client.battle.artists_battle_handlers import get_tracks_for_artists_battle
from madnessbracket.client.secret.themes.artists_battle.matchups import pick_random_artists_matchup
from madnessbracket.schemas.response import TracksInfoResponse
from madnessbracket.track_processing.track_processing_helpers import make_tracks_info_response


def get_secret_artists_battle(bracket_limit: int = 16) -> TracksInfoResponse:
    """
    get 'secret' artists battle from a hand-picked list of spicy matchups (e.g. Gorillaz vs Blur, RS vs Beatles, etc.)
    :param bracket_limit: (int) bracket's upper limit
    :return: (TracksInfoResponse) with all the secret theme bracket info
    """
    artist_1_name, artist_2_name = pick_random_artists_matchup()
    # pick from the selection of top 50 tracks only
    MAX_SONGS_RANGE = 50
    battle_tracks = get_tracks_for_artists_battle(artist_1_name, artist_2_name, bracket_limit, MAX_SONGS_RANGE)
    tracks_info_response = make_tracks_info_response(
        tracks=battle_tracks,
        description=f"{artist_1_name.upper()} vs {artist_2_name.upper()}",
        value1=artist_1_name,
        value2=artist_2_name,
        extra="artists_battle"
    )
    return tracks_info_response
