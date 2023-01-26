import random
from typing import Optional

from madnessbracket.client.database_manipulation.db_artist_handlers import db_get_artist
from madnessbracket.client.database_manipulation.db_track_handlers import \
    db_get_artist_most_popular_song_by_artist_entry
from madnessbracket.client.trivia.commentaries.general_commentary import GENERAL_COMMENTARY_LIST
from madnessbracket.client.trivia.commentaries.popular_commentary import POPULAR_COMMENTARY_LIST
from madnessbracket.client.trivia.commentaries.special_commentary import SPECIAL_COMMENTARY_LIST
from madnessbracket.models import Artist


class CommentaryGenerator:
    COMMENTARY_FREQUENCY = {
        "special": [True],
        "popular": [True, False],
        "general": [True] + [False] * 5,
    }

    def __init__(self, song_title: str, artist_name: str):
        self.song_title = song_title
        self.artist_name = artist_name

    def _calculate_probability(self, commentary_type: str) -> bool:
        """
        'roll a dice' for each category (commentary type) based on their predefined frequency/probability
        :param commentary_type: (str) type of commentary to roll a dice for to get a chance
        :return: (bool) True/False
        """
        return random.choice(self.COMMENTARY_FREQUENCY[commentary_type])

    def _get_random_general_commentary(self) -> Optional[str]:
        """
        get random 'general' commentary; i.e. not based on anything particular, a little banter comment
        :return: (str) random general commentary (on success)
        """
        success = self._calculate_probability("general")
        return random.choice(GENERAL_COMMENTARY_LIST) if success else None

    def _get_special_commentary(self, commentaries: list[str]) -> Optional[str]:
        """
        get random 'special' commentary; i.e. specifically created for songs/artists, etc.
        :return: (str) random special commentary (on success)
        """
        success = self._calculate_probability("special")
        return random.choice(commentaries) if success else None

    def _get_random_popular_commentary(self) -> Optional[str]:
        """
        get random 'popular' commentary;
            i.e. a comment for the songs considered popular for the given artist (most listened song)
        :return: (str) random special commentary (on success)
        """
        success = self._calculate_probability("popular")
        return random.choice(POPULAR_COMMENTARY_LIST) if success else None

    def _find_special_commentaries(self) -> Optional[list[str]]:
        """
        try to find 'special' commentaries within a dict of commentaries;
            i.e. specifically created for songs/artists, etc.
        used for easter eggs / taunting the user
        :return: (list[str]) a list of special comments if there are any for the given (song, artist) pair
        """
        try:
            commentaries = SPECIAL_COMMENTARY_LIST[self.artist_name.lower()][self.song_title.lower()]
        except (KeyError, ValueError):
            return None
        return commentaries

    def _is_song_most_popular(self, artist_entry: Artist) -> bool:
        """
        find out if the song is the most popular for the artist
        :param artist_entry: (Artist) artist object in db
        :return: (bool) True if the most popular for the artist, False otherwise
        """
        most_popular_song = db_get_artist_most_popular_song_by_artist_entry(artist_entry)
        if not most_popular_song:
            return False
        if most_popular_song.title.lower() == self.song_title.lower():
            return True
        return False

    def get_commentary(self) -> Optional[str]:
        """
        get 'Easter egg' commentary for the given song
        :return: (str) commentary on success
        """
        artist_entry = db_get_artist(self.artist_name)
        if not artist_entry:
            return self._get_random_general_commentary()

        special_commentaries = self._find_special_commentaries()
        if special_commentaries:
            return self._get_special_commentary(special_commentaries)

        if self._is_song_most_popular(artist_entry):
            return self._get_random_popular_commentary()

        return self._get_random_general_commentary()
