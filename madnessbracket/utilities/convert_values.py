from datetime import datetime
from typing import Union, Optional


def parse_release_date(release_date: Union[str, int], forced_parsing: bool = False) -> Optional[datetime]:
    """
    parse datetime str into datetime object (extract Year)
    :param release_date: a datetime str
    :param forced_parsing: get an arbitrary date anyway (used for forced sorting by dates to avoid any exceptions)
    :return: datetime object (year)
    """
    if not isinstance(release_date, datetime):
        if isinstance(release_date, int):
            release_date = str(release_date)
        try:
            release_date = datetime.strptime(release_date[:4], '%Y')
        except (ValueError, TypeError) as e:
            print(e)
            if forced_parsing:
                return datetime(1970, 1, 1)
            return None
    return release_date
