import discogs_client
from flask import current_app


def get_discogs_client() -> discogs_client.Client:
    """
    get a discogs client object
    :return: discogs client
    """
    discogs = discogs_client.Client(
        user_agent=current_app.config['APP_NAME'],
        user_token=current_app.config['DISCOGS_USER_TOKEN']
    )
    return discogs
