from madnessbracket.client.secret.secret_theme_generator import SecretThemeGenerator
from madnessbracket.schemas.response import TracksInfoResponse


def get_tracks_for_secret(bracket_limit: int = 16) -> TracksInfoResponse:
    """
    get tracks for a 'secret' theme;
    hand-picked tracks for a particular secret theme: artist's anniversary, memes, genres battle, soundtracks, etc.
    :param bracket_limit: bracket's upper limit
    :return: (TracksInfoResponse) with all the bracket info
    """
    secret_theme = SecretThemeGenerator(bracket_limit)
    tracks = secret_theme.get_secret_theme_info()
    return tracks
