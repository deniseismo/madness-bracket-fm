import json

import requests


def lastfm_show_response_error(response: requests.Response) -> bool:
    """
    display error message from lastfm response
    :param response: response from lastfm
    """
    try:
        error_response = response.json()
        error_message = error_response["message"]
        print(error_message)
    except (KeyError, TypeError, json.decoder.JSONDecodeError) as e:
        print(e)
        return False
    return True
