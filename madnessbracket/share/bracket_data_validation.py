import uuid
from typing import List
from pydantic import BaseModel, ValidationError, NoneStr, Field


def validate_bracket_data_for_sharing(bracket_data):
    """
    validate bracket data coming from front-end when sharing
    checks structure & data type using pydantic library
    """
    class Track(BaseModel):
        """
        Track data with all the info about the song
        """
        track_title: str
        spotify_preview_url: NoneStr = None
        text_color: NoneStr = None
        album_colors: list = None

    class Cell(BaseModel):
        round_index: int = Field(alias="roundIndex")
        song: dict
        advanceable: bool
        active: bool
        album_colors: list = Field(default=None, alias="albumColors")
        text_color: str = Field(default=None, alias="textColor")
        track_id: int = Field(default=None, alias="trackID")

    class FinalRound(BaseModel):
        left: Cell
        right: Cell
        winner: Cell

    class Structure(BaseModel):
        """
        bracket structure 
        """
        left: dict
        right: dict
        final: FinalRound

    class Bracket(BaseModel):
        description: str
        tracks: List[Track]
        structure: Structure

    try:
        bracket = Bracket(**bracket_data)
        print('YEEES!')
        # print(bracket)
        # print(bracket.structure.final)
        print(dir(bracket.structure))
        return bracket
    except ValidationError as e:
        print(e.json())
        return None


def parse_bracket_data_for_sharing(bracket_data):
    """gets bracket data ready for sharing
    parses pydantic dict-like structures to ready'em up for sharing
    Args:
        bracket_data (dict): pydantic dict-like model with all the info about the bracket

    Returns:
        (dict): parsed dict with bracket data for sharing
    """
    parsed_bracket_data = {
        "title": bracket_data.description,
        "bracket_info": {
            "tracks": [track.dict() for track in bracket_data.tracks],
            "structure": {
                "left": bracket_data.structure.left,
                "right": bracket_data.structure.right,
                "final": {
                    "left": bracket_data.structure.final.left.dict(by_alias=True),
                    "right": bracket_data.structure.final.right.dict(by_alias=True),
                    "winner": bracket_data.structure.final.winner.dict(by_alias=True)
                }
            }
        },
        "winner": bracket_data.structure.final.winner.song["songName"]
    }
    print("-" * 5, "parsing", "-" * 5)
    print(parsed_bracket_data)
    print(parsed_bracket_data["title"])
    print("-" * 10)
    return parsed_bracket_data


def is_valid_uuid(uuid_string_to_check):
    """checks if a given string is a valid uuid4 string

    Args:
        uuid_string_to_check (str): [description]

    Returns:
        (bool): true if valid, false otherwise
    """
    try:
        uuid_obj = uuid.UUID(uuid_string_to_check, version=4)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_string_to_check
