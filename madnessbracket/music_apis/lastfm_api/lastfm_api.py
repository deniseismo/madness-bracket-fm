import requests_cache
import requests

from flask import current_app

requests_cache.install_cache()


def lastfm_get_response(payload: dict):
    """
    get response
    :param: payload: a dict with all the info on a particular request
    """
    # define headers and URL
    headers = {'user-agent': current_app.config['LASTFM_USER_AGENT']}
    url = 'http://ws.audioscrobbler.com/2.0/'
    # Add API key and format to the payload
    payload['api_key'] = current_app.config['LASTFM_API_KEY']
    payload['format'] = 'json'
    response = requests.get(url, headers=headers, params=payload)
    return response


