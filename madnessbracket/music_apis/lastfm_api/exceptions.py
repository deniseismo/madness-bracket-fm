class LastFMCriticalError(Exception):
    pass


class LastFMNoUserFoundError(LastFMCriticalError):
    pass


class LastFMNotEnoughTracksError(Exception):
    pass
