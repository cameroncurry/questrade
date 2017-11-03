#
# Copyright Cameron Curry (c) 2017
#

from . import qt_request


class QTService:

    def __init__(self, qt_access):
        self._qt_access = qt_access

    def _headers(self):
        return {
            'Authorization': '{} {}'.format(self._qt_access.token_type, self._qt_access.access_token)
        }

    def _get(self, endpoint, params=None, **kwargs):
        url = '{}{}'.format(self._qt_access.api_server, endpoint)
        return qt_request.get(url, params, headers=self._headers(), **kwargs)
