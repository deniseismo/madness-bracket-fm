from typing import Optional

from madnessbracket.track_processing.track_preparation import prepare_tracks_for_artist_battle
from madnessbracket.client.artist.artist_handlers import get_artists_tracks
from madnessbracket.schemas.track_schema import TrackInfo


def get_tracks_for_artists_battle(
        artist_1_name: str,
        artist_2_name: str,
        bracket_limit: int,
        max_songs_range: int = 100
) -> Optional[list[TrackInfo]]:
    """
    get tracks for ARTIST BATTLE: ARTIST 1 vs ARTIST 2 (e.g. Radiohead vs Muse)
    :param artist_1_name: (str) first artist's name
    :param artist_2_name: (str) second artist's name
    :param bracket_limit: (int) chosen bracket upper limit
    :param max_songs_range: (int) maximum number of top songs to choose from, defaults to top 100
    :return: (list[TrackInfo]) a list of TrackInfo with all the information needed for artists battle
    """
    if not artist_1_name or not artist_2_name or not bracket_limit:
        return None
    artist_1_tracks = get_artists_tracks(artist_1_name, bracket_limit, max_songs_range)
    if not artist_1_tracks:
        print(f"could not find tracks for {artist_1_name}")
        return None
    artist_2_tracks = get_artists_tracks(artist_2_name, bracket_limit, max_songs_range)
    if not artist_2_tracks:
        print(f"could not find tracks for {artist_2_name}")
        return None
    battle_tracks = prepare_tracks_for_artist_battle(artist_1_tracks, artist_2_tracks, bracket_limit)
    return battle_tracks
