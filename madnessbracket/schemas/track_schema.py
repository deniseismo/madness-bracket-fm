from dataclasses import dataclass

from madnessbracket.schemas.info_base import InfoBase


@dataclass
class TrackInfo(InfoBase):
    """
    stores all the information about track that will be sent to the user
    :attr track_title: (str) album's title
    :attr artist_name: (str) artist's name
    :attr spotify_preview_url: (str) a link to spotify preview (30-second free audio sample of a song)
    :attr album_colors: (list[str]) a list of album's most dominant colors (in hex)
    :attr text_color: (str) release date
    """
    track_title: str
    artist_name: str
    spotify_preview_url: str = None
    album_colors: list[str] = None
    text_color: str = "white"

    def __repr__(self):
        album_description = f"Song({self.track_title}) by Artist({self.artist_name})"
        return album_description
