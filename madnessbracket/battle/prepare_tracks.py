import random

from madnessbracket.musician.prepare_tracks import add_text_color_to_tracks
from madnessbracket.utilities.bracket_sizing import get_capped_bracket_size


def prepare_tracks_for_artist_battle(artist_1_tracks, artist_2_tracks, bracket_size):
    """
    prepare (cap & randomize) tracks for the battle of artists
    :param artist_1_tracks: tracks by artist 1
    :param artist_2_tracks: tracks by artist 2
    :param bracket_size:
    :return:
    """
    min_number_of_tracks = min([len(artist_1_tracks), len(artist_2_tracks)])
    tracks_cap = get_capped_bracket_size(min_number_of_tracks, bracket_size)
    song_count_per_artist = int(tracks_cap / 2)
    random.shuffle(artist_1_tracks)
    random.shuffle(artist_2_tracks)
    artist_1_tracks_processed = artist_1_tracks[:song_count_per_artist]
    artist_2_tracks_processed = artist_2_tracks[:song_count_per_artist]
    battle_tracks = []
    for matchup in zip(artist_1_tracks_processed, artist_2_tracks_processed):
        track_a, track_b = matchup
        battle_tracks.append(track_a)
        battle_tracks.append(track_b)
    add_text_color_to_tracks(battle_tracks)
    return battle_tracks
