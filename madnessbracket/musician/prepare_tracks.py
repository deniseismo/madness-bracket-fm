from madnessbracket.dev.db_mgmt.color_mgmt.dominant_colors import get_image_dominant_colors_via_image_url
from madnessbracket.utilities.bracket_sizing import get_capped_bracket_size
from madnessbracket.utilities.color_processing import get_contrast_color_for_two_color_gradient
from madnessbracket.utilities.track_filtering import get_filtered_name
from madnessbracket.utilities.track_randomization import get_weighted_random_selection_of_tracks


def prepare_tracks_for_musician(tracks: dict, limit=16):
    """
    randomizes & caps (at a given limit, default=32) tracks/songs;
    uses weighted random selection for better sorting/randomization
    :param limit: maximum number of tracks in a bracket
    :param tracks: a tracks dict with the list of 'track info' dicts
    :return: randomized & capped tracks
    """
    if not tracks:
        return None
    number_of_tracks = len(tracks['tracks'])
    print('total amount of tracks: ', number_of_tracks)
    tracks_cap = get_capped_bracket_size(number_of_tracks, limit)
    randomized_tracks = get_weighted_random_selection_of_tracks(
        tracks['tracks'], tracks_cap)
    if not randomized_tracks:
        return None
    add_text_color_to_tracks(randomized_tracks)
    tracks['tracks'] = randomized_tracks
    return tracks


def add_text_color_to_tracks(tracks: list):
    """
    dynamically add the most appropriate contrast text color,
    so that text's readable  (where applicable)
    :param tracks: a list of dicts with all the needed info about songs/tracks
    :return:
    """
    if not tracks:
        return None
    for track in tracks:
        if not track["album_colors"]:
            continue
        album_colors = track["album_colors"]
        try:
            dominant_color = album_colors[0]
            secondary_color = album_colors[1]
            text_color = get_contrast_color_for_two_color_gradient(
                dominant_color, secondary_color)
            track["text_color"] = text_color
        except (ValueError, IndexError) as e:
            print(e)


def process_tracks_from_db(tracks: list):
    processed_tracks = []
    for track_entry in tracks:
        track = process_a_track_from_db(track_entry)
        processed_tracks.append(track)
    return processed_tracks


def process_a_track_from_db(track_entry):
    """
    gets all the needed info about the track from track entry (Song object)
    :param track_entry: a Song instance
    :return: dict with track info
    """
    try:
        album_colors = track_entry.album.album_cover_color.split(",")
    except (AttributeError, NameError, TypeError, IndexError) as e:
        print(e)
        album_colors = None
    track = {
        "track_title": track_entry.title,
        "artist_name": track_entry.artist.name,
        "spotify_preview_url": track_entry.spotify_preview_url if track_entry.spotify_preview_url else None,
        "album_colors": album_colors,
        "text_color": "white"
    }
    return track


def process_tracks_from_spotify(tracks: list):
    processed_tracks = []
    track_titles = set()
    for track_entry in tracks:
        track_title = get_filtered_name(track_entry.name)
        if track_title in track_titles:
            continue
        track_titles.add(track_title)
        track = process_a_track_from_spotify(track_entry)
        processed_tracks.append(track)
    return processed_tracks


def process_a_track_from_spotify(track_entry):
    """
    gets all the needed info about the track from track entry (FullTrack tekore object)
    :param track_entry: a FullTrack tekore instance
    :return: dict with track info
    """
    try:
        album_image_url = track_entry.album.images[-1].url
        album_colors = get_image_dominant_colors_via_image_url(
            album_image_url)
    except (IndexError, ValueError) as e:
        print(e)
        album_colors = None
    track = {
        "track_title": get_filtered_name(track_entry.name),
        "artist_name": track_entry.artists[0].name,
        "spotify_preview_url": track_entry.preview_url if track_entry.preview_url else None,
        "album_colors": album_colors
    }
    return track
