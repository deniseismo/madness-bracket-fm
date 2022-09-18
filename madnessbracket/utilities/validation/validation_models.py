from pydantic import validator, BaseModel, Field, NoneStr


class LastFMUsername(BaseModel):
    """
    validation model for user input in lastfm route; validates username and time period picked by user
    """
    name: str

    @classmethod
    @validator("name")
    def is_valid_username(cls, v: str) -> str:
        v = v.strip()
        if not (1 < len(v) < 16):
            raise ValueError("incorrect username length; must be at least 2 characters long and at most 16 chars.")
        return v


class ArtistName(BaseModel):
    """
    validation model for validating artist's name picked by user
    """
    name: str

    @classmethod
    @validator("name")
    def is_valid_artist_name(cls, v: str) -> str:
        v = v.strip()
        if not (0 < len(v) < 100):
            raise ValueError("incorrect artist name; must be at least 1 character long and at most 100 chars.")
        return v


class BracketUpperLimit(BaseModel):
    limit: int

    @classmethod
    @validator("limit")
    def is_valid_bracket_upper_limit(cls, v: str) -> str:
        valid_limits = [4, 8, 16, 32]
        if v not in valid_limits:
            raise ValueError("incorrect bracket limit")
        return v


class BracketTrack(BaseModel):
    track_title: str
    artist_name: str
    spotify_preview_url: NoneStr = None
    text_color: NoneStr = None
    album_colors: list = None


class BracketCell(BaseModel):
    round_index: int = Field(alias="roundIndex")
    advanceable: bool
    active: bool
    track_id: int = Field(default=None, alias="trackID")
    loser: bool
    # song: dict
    # album_colors: list = Field(default=None, alias="albumColors")
    # text_color: str = Field(default=None, alias="textColor")


class BracketFinalRound(BaseModel):
    left: BracketCell
    right: BracketCell
    winner: BracketCell


class BracketStructure(BaseModel):
    """
    bracket structure
    """
    left: dict
    right: dict
    final: BracketFinalRound


class SharedBracketData(BaseModel):
    bracket_type: str = Field(alias="bracketType")
    value1: NoneStr = None
    value2: NoneStr = None
    description: str
    extra: NoneStr = None
    tracks: list[BracketTrack]
    structure: BracketStructure


class WinnerTrackBracketData(BaseModel):
    artist_name: str
    song_title: str
    bracket_type: NoneStr = None
    description: NoneStr = None
