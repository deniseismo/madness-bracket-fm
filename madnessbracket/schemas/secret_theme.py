from madnessbracket.schemas.info_base import InfoBase
from madnessbracket.schemas.track_schema import TrackInfo


class SecretTracksInfo(InfoBase):
    """
    dataclass used to store information about secret them and its tracks (processed & ready for madness bracket)

    :attr theme: (str) secret theme description
    :attr tracks: (list[TrackInfo]) list of secret tracks (processed as TrackInfo objects)
    :attr extra: (str) extra information about bracket type (e.g. artists battle)
    """
    theme: str
    tracks: list[TrackInfo]
    extra: str = None
