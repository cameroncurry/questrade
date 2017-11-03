#
# Copyright Cameron Curry (c) 2017
#

from ..common import cast, qt_str


class QTAccess:

    def __init__(self, access_token=None, token_type=None, expires_in=None, refresh_token=None, api_server=None):
        self._access_token = access_token
        self._token_type = token_type
        self._expires_in = expires_in
        self._refresh_toke = refresh_token
        self._api_server = api_server

    @property
    def access_token(self):
        return self._access_token

    @property
    def token_type(self):
        return self._token_type

    @property
    def expires_in(self):
        return self._expires_in

    @property
    def refresh_token(self):
        return self._refresh_toke

    @property
    def api_server(self):
        return self._api_server

    def __str__(self):
        return qt_str(self)

    @classmethod
    def from_json(cls, json):
        return cls(access_token=json.get("access_token"),
                   token_type=json.get("token_type"),
                   expires_in=cast(json.get("expires_in"), int),
                   refresh_token=json.get("refresh_token"),
                   api_server=json.get("api_server"))
