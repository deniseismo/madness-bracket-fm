import json
from dataclasses import asdict, dataclass, astuple
from datetime import datetime


@dataclass
class InfoBase(json.JSONEncoder):
    """
    base dataclass for all kind of information dataclasses
    """
    def default(self, o):
        print("_" * 10)
        """serialize data © tekore"""
        if isinstance(o, datetime):
            return str(o.year)
        elif isinstance(o, InfoBase):
            return asdict(o)
        else:
            return super().default(o)

    def __iter__(self):
        return iter(astuple(self))

    def to_dict(self):
        return asdict(self)
