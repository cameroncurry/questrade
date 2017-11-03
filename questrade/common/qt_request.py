#
# Copyright Cameron Curry (c) 2017
#

import requests

from .error import QTError
from .error import QTTokenInvalidError


def get(url, params=None, **kwargs):
    """
    Returns requests Response if status code is OK, otherwise throws Questrade Exception.
    
    :param url: 
    :param params: 
    :param kwargs: 
    :return: Response
    """
    r = requests.get(url, params=params, **kwargs)
    if r.status_code == 200:
        return r
    else:
        _throw_qt_exception(r)


def _throw_qt_exception(response):
    if 'application/json' in response.headers.get('Content-Type'):
        response_json = response.json()
        qt_code = int(response_json['code'])
        message = response_json['message']

        if response.status_code == 401 and qt_code == 1017:
            raise QTTokenInvalidError(response.status_code, qt_code, message)
    else:
        raise QTError(response.status_code, response.text)
