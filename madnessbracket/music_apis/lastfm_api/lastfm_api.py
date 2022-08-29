from typing import Optional

import requests
from flask import current_app


def lastfm_get_response(payload: dict) -> Optional[requests.Response]:
    """
    get a response from lastfm given some payload info
    :param: payload: (dict) a dict with all the info on a particular request
    """
    # define headers and URL
    headers = {'user-agent': current_app.config['LASTFM_USER_AGENT']}
    url = 'http://ws.audioscrobbler.com/2.0/'
    # Add API key and format to the payload
    payload['api_key'] = current_app.config['LASTFM_API_KEY']
    payload['format'] = 'json'
    try:
        response = requests.get(url, headers=headers, params=payload)
        print(f"{response=}")
    except requests.exceptions.ConnectionError as e:
        print(e)
        return None
    return response
