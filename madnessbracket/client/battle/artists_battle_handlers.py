from typing import Optional

from madnessbracket.track_processing.track_preparation import prepare_tracks_for_artist_battle
from madnessbracket.client.musician.musician_handlers import get_artists_tracks
from madnessbracket.schemas.track_schema import TrackInfo


def get_tracks_for_artists_battle(
        artist_1_name: str,
        artist_2_name: str,
        bracket_limit: int
) -> Optional[list[TrackInfo]]:
    """
    get tracks for ARTIST BATTLE: ARTIST 1 vs ARTIST 2 (e.g. Radiohead vs Muse)
    :param artist_1_name: (str) first artist's name
    :param artist_2_name: (str) second artist's name
    :param bracket_limit: (int) chosen bracket upper limit
    :return: (list[TrackInfo]) a list of TrackInfo with all the information needed for artists battle
    """
    if not artist_1_name or not artist_2_name or not bracket_limit:
        return None
    artist_1_tracks = get_artists_tracks(artist_1_name, bracket_limit)
    if not artist_1_tracks:
        print(f"could not find tracks for {artist_1_name}")
        return None
    artist_2_tracks = get_artists_tracks(artist_2_name, bracket_limit)
    if not artist_2_tracks:
        print(f"could not find tracks for {artist_2_name}")
        return None
    battle_tracks = prepare_tracks_for_artist_battle(artist_1_tracks, artist_2_tracks, bracket_limit)
    return battle_tracks
