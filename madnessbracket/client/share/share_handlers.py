from madnessbracket.utilities.validation.validation_models import SharedBracketData


def parse_bracket_data_for_sharing(bracket_data: SharedBracketData) -> dict:
    """
    parse bracket data for saving it in database
    :param bracket_data: (SharedBracketData) pydantic-validated bracket data from the user
    :return: (dict) parsed bracket data ready for saving
    """
    parsed_bracket_data = {
        "bracket_type": bracket_data.bracket_type,
        "title": bracket_data.description,
        "value1": bracket_data.value1,
        "value2": bracket_data.value2,
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
        "winner": None,
        "extra": bracket_data.extra
    }
    if bracket_data.structure.final.winner.track_id:
        track_id = bracket_data.structure.final.winner.track_id
        parsed_bracket_data["winner"] = bracket_data.tracks[track_id].track_title
    return parsed_bracket_data
