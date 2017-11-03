#
# Copyright Cameron Curry (c) 2017
#

from ..common import cast, qt_str


class QTAccount:

    def __init__(self, account_type=None, number=None, status=None,
                 is_primary=None, is_billing=None, client_account_type=None):
        self._account_type = account_type
        self._number = number
        self._status = status
        self._is_primary = is_primary
        self._is_billing = is_billing
        self._client_account_type = client_account_type

    @property
    def account_type(self):
        return self._account_type

    @property
    def number(self):
        return self._number

    @property
    def status(self):
        return self._status

    @property
    def is_primary(self):
        return self._is_primary

    @property
    def is_billing(self):
        return self._is_billing

    @property
    def client_account_type(self):
        return self._client_account_type

    def __str__(self):
        return qt_str(self)

    @classmethod
    def from_json(cls, json):
        return cls(account_type=json.get('type'),
                   number=cast(json.get('number'), int),
                   status=json.get('status'),
                   is_primary=cast(json.get('isPrimary'), bool),
                   is_billing=cast(json.get('isBilling'), bool),
                   client_account_type=json.get('clientAccountType'))
