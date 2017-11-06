#
# Copyright Cameron Curry (c) 2017
#

from datetime import datetime, timezone

from ..common import QTService
from .qt_account import QTAccount
from .qt_activity import QTActivity


class QTAccountService(QTService):

    def accounts(self):
        r = self._get('v1/accounts')
        accounts_json = r.json()
        return [QTAccount.from_json(account) for account in accounts_json['accounts']]

    def activities(self, account_number, start_datetime: datetime, end_datetime: datetime):
        if start_datetime.tzinfo is None:
            start_datetime = start_datetime.replace(tzinfo=timezone.utc)

        if end_datetime.tzinfo is None:
            end_datetime = end_datetime.replace(tzinfo=timezone.utc)

        r = self._get('v1/accounts/{}/activities'.format(account_number),
                      params={'startTime': start_datetime.isoformat(),
                              'endTime': end_datetime.isoformat()})
        activities_json = r.json()
        return [QTActivity.from_json(activity) for activity in activities_json['activities']]
