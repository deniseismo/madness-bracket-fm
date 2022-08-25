import discogs_client
from flask import current_app


def get_discogs_client():
    """gets authed discogs client

    Returns:
        authed discogs client
    """
    discogs = discogs_client.Client(
        user_agent=current_app.config['APP_NAME'], user_token=current_app.config['DISCOGS_USER_TOKEN'])
    return discogs
