#
# Copyright Cameron Curry (c) 2017
#

from ..common import QTService
from .qt_account import QTAccount


class QTAccountService(QTService):

    def accounts(self):
        r = self._get('v1/accounts')
        accounts_json = r.json()
        return [QTAccount.from_json(account) for account in accounts_json['accounts']]
