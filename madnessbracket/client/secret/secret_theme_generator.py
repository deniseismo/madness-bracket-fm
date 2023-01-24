import random

from madnessbracket.client.secret.themes.artists_battle.artists_battle_handlers import get_secret_artists_battle
from madnessbracket.client.secret.themes.disney_soundtrack.get_disney_tracks import get_secret_disney_tracks
from madnessbracket.client.secret.themes.eurovision.get_eurovision_tracks import get_secret_eurovision_tracks
from madnessbracket.client.secret.themes.pattern_in_the_title.get_number_tracks import get_secret_number_tracks
from madnessbracket.client.secret.themes.pattern_in_the_title.get_question_mark_tracks import get_secret_question_mark_tracks
from madnessbracket.client.secret.themes.spotify_playlist.get_playlist_tracks import get_seismo_top_tracks_of_2021
from madnessbracket.schemas.response import TracksInfoResponse


class SecretThemeGenerator:
    THEMES = (
        "artists_battle",
        "disney_soundtrack",
        "eurovision",
        "numbers",
        "questions",
        "seismo_top_2021",
    )
    THEME_HANDLERS = {
        "artists_battle": get_secret_artists_battle,
        "disney_soundtrack": get_secret_disney_tracks,
        "eurovision": get_secret_eurovision_tracks,
        "numbers": get_secret_number_tracks,
        "questions": get_secret_question_mark_tracks,
        "seismo_top_2021": get_seismo_top_tracks_of_2021,
    }

    def __init__(self, bracket_size: int, themes_list: tuple[str] = THEMES):
        self.bracket_size = bracket_size
        self.themes = themes_list

    def _pick_random_theme(self) -> str:
        """
        select random secret theme from a list of themes
        :return: (str) secret theme's title
        """
        return random.choice(self.themes)

    def get_secret_theme_info(self) -> TracksInfoResponse:
        """
        load secret theme bracket info with all the tracks, description, etc.
        :return: (TracksInfoResponse) with all the secret theme bracket info
        """
        random_theme = self._pick_random_theme()
        tracks = self.THEME_HANDLERS[random_theme](self.bracket_size)
        return tracks
