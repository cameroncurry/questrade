#
# Copyright Cameron Curry (c) 2017
#

from datetime import datetime, timezone, timedelta
from unittest import TestCase
from unittest.mock import patch

from questrade.access import QTAccess
from questrade.account import QTAccount
from questrade.account import QTBalance
from questrade.account import QTActivity
from questrade.account import QTAccountService
from questrade.common.error import QTTokenInvalidError


class TestQTAccountService(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.qt_access = QTAccess(access_token='C3lTUKuNQrAAmSD/TPjuV/HI7aNrAwDp',
                                 token_type='Bearer',
                                 expires_in=300,
                                 refresh_token='aSBe7wAAdx88QTbwut0tiu3SYic3ox8F',
                                 api_server='https://api01.iq.questrade.com/')

        cls.account_service = QTAccountService(cls.qt_access)

    @patch('requests.get')
    def test_accounts(self, mock):
        mock.return_value.ok = True
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {
            'accounts': [
                {
                    'type': 'Margin',
                    'number': 26598145,
                    'status': 'Active',
                    'isPrimary': 'true',
                    'isBilling': 'true',
                    'clientAccountType': 'Individual'
                }
            ]
        }
        mock.return_value.headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }

        accounts = self.account_service.accounts()
        self.assertEqual(len(accounts), 1)
        self.assertIsInstance(accounts[0], QTAccount)
        expected_accounts = (
            (accounts[0].account_type, 'Margin'),
            (accounts[0].number, 26598145),
            (accounts[0].status, 'Active'),
            (accounts[0].is_primary, True),
            (accounts[0].is_billing, True),
            (accounts[0].client_account_type, 'Individual')
        )
        for result, expected in expected_accounts:
            with self.subTest(result=result):
                self.assertEqual(result, expected)

        mock.assert_called_with('https://api01.iq.questrade.com/v1/accounts',
                                params=None,
                                headers={'Authorization': 'Bearer C3lTUKuNQrAAmSD/TPjuV/HI7aNrAwDp'})

    @patch('requests.get')
    def test_access_token_expired(self, mock):
        mock.return_value.ok = False
        mock.return_value.status_code = 401
        mock.return_value.json.return_value = {
            'code': '1017',
            'message': 'Access token is invalid',
        }
        mock.return_value.headers = {'Content-Type': 'application/json; charset=utf-8'}

        with self.assertRaises(QTTokenInvalidError):
            self.account_service.accounts()

    @patch('requests.get')
    def test_balances(self, mock):
        mockCAD = {
            'currency': 'CAD',
            'cash': 243971.7,
            'marketValue': 6017,
            'totalEquity': 249988.7,
            'buyingPower': 496367.2,
            'maintenanceExcess': 248183.6,
            'isRealTime': 'false'
        }
        mockUSD = {
            'currency': 'USD',
            'cash': 243971.7,
            'marketValue': 6017,
            'totalEquity': 249988.7,
            'buyingPower': 496367.2,
            'maintenanceExcess': 248183.6,
            'isRealTime': 'false'
        }
        mock.return_value.ok = True
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {
            'perCurrencyBalances': [mockCAD, mockUSD],
            'combinedBalances': [mockCAD, mockUSD],
            'sodPerCurrencyBalances': [mockCAD, mockUSD],
            'sodCombinedBalances': [mockCAD, mockUSD]
        }
        mock.return_value.headers = {'Content-Type': 'application/json; charset=utf-8'}

        account_number = 26598145
        qt_balances = self.account_service.balances(account_number)
        self.assertEqual(len(qt_balances), 8)

        for qt_balance, currency, balance_type in zip(qt_balances, ['CAD', 'USD'] * 4,
                                                      [QTBalance.BalanceType.PER_CURRENCY] * 2 +
                                                      [QTBalance.BalanceType.COMBINED] * 2 +
                                                      [QTBalance.BalanceType.SOD_PER_CURRENCY] * 2 +
                                                      [QTBalance.BalanceType.SOD_COMBINED] * 2):
            self.assertIsInstance(qt_balance, QTBalance)
            expected_balances = (
                (qt_balance.balance_type, balance_type),
                (qt_balance.currency, currency),
                (qt_balance.cash, 243971.7),
                (qt_balance.market_value, 6017),
                (qt_balance.total_equity, 249988.7),
                (qt_balance.buying_power, 496367.2),
                (qt_balance.maintenance_excess, 248183.6),
                (qt_balance.is_real_time, False)
            )
            for result, expected in expected_balances:
                with self.subTest(result=result):
                    self.assertEqual(result, expected)

    @patch('requests.get')
    def test_activities(self, mock):
        mock.return_value.ok = True
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {
            'activities': [
                {
                    'tradeDate': '2011-02-16T00:00:00.000000-05:00',
                    'transactionDate': '2011-02-16T00:00:00.000000-05:00',
                    'settlementDate': '2011-02-16T00:00:00.000000-05:00',
                    'action': '',
                    'symbol': '',
                    'symbolId': 0,
                    'description': 'INT FR 02/04 THRU02/15@ 4 3/4%BAL  205,006   AVBAL  204,966 ',
                    'currency': 'USD',
                    'quantity': 0,
                    'price': 0,
                    'grossAmount': 0,
                    'commission': 0,
                    'netAmount': -320.08,
                    'type': 'Interest'
                }
            ]
        }
        mock.return_value.headers = {'Content-Type': 'application/json; charset=utf-8'}

        account_number = 26598145
        start = datetime(2011, 2, 1, tzinfo=timezone(timedelta(hours=-5)))
        end = datetime(2011, 2, 28, tzinfo=timezone(timedelta(hours=-5)))

        qt_activities = self.account_service.activities(account_number, start, end)
        self.assertEqual(len(qt_activities), 1)
        self.assertIsInstance(qt_activities[0], QTActivity)
        expected_activities = (
            (qt_activities[0].trade_date, datetime(2011, 2, 16, tzinfo=timezone(timedelta(hours=-5)))),
            (qt_activities[0].transaction_date, datetime(2011, 2, 16, tzinfo=timezone(timedelta(hours=-5)))),
            (qt_activities[0].settlement_date, datetime(2011, 2, 16, tzinfo=timezone(timedelta(hours=-5)))),
            (qt_activities[0].action, ''),
            (qt_activities[0].symbol, ''),
            (qt_activities[0].symbol_id, 0),
            (qt_activities[0].description, 'INT FR 02/04 THRU02/15@ 4 3/4%BAL  205,006   AVBAL  204,966 '),
            (qt_activities[0].currency, 'USD'),
            (qt_activities[0].quantity, 0),
            (qt_activities[0].price, 0.0),
            (qt_activities[0].gross_amount, 0.0),
            (qt_activities[0].commission, 0.0),
            (qt_activities[0].net_amount, -320.08),
            (qt_activities[0].activity_type, 'Interest')
        )
        for result, expected in expected_activities:
            with self.subTest(result=result):
                self.assertEqual(result, expected)

        mock.assert_called_with('https://api01.iq.questrade.com/v1/accounts/26598145/activities',
                                params={'startTime': '2011-02-01T00:00:00-05:00',
                                        'endTime': '2011-02-28T00:00:00-05:00'},
                                headers={'Authorization': 'Bearer C3lTUKuNQrAAmSD/TPjuV/HI7aNrAwDp'})
