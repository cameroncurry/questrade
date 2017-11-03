#
# Copyright Cameron Curry (c) 2017
#

from ..config import qt_login_url
from ..common import qt_request

from .qt_access import QTAccess


class QTAccessService:

    @staticmethod
    def refresh(refresh_token: str):
        r = qt_request.get(qt_login_url, params={'grant_type': 'refresh_token', 'refresh_token': refresh_token})
        return QTAccess.from_json(r.json())
