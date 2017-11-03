#
# Copyright Cameron Curry (c) 2017
#

from unittest import TestCase
from unittest.mock import patch

from questrade.access import QTAccess
from questrade.account import QTAccount
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

    @patch('requests.get')
    def test_accounts(self, mock):
        mock.return_value.ok = True
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {
            'accounts': [
                {
                    'type': 'Margin',
                    'number': '26598145',
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

        account_service = QTAccountService(self.qt_access)
        accounts = account_service.accounts()

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

        account_service = QTAccountService(self.qt_access)

        with self.assertRaises(QTTokenInvalidError):
            account_service.accounts()
