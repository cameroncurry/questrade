#
# Copyright Cameron Curry (c) 2017
#

from unittest import TestCase
from unittest.mock import patch

from questrade.common.error import QTError
from questrade.access import QTAccess
from questrade.access import QTAccessService


class TestQtAccessService(TestCase):

    @patch('requests.get')
    def test_access_granted(self, mock):
        mock.return_value.ok = True
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {
            'access_token': 'C3lTUKuNQrAAmSD/TPjuV/HI7aNrAwDp',
            'token_type': 'Bearer',
            'expires_in': '300',
            'refresh_token': 'aSBe7wAAdx88QTbwut0tiu3SYic3ox8F',
            'api_server': 'https://api01.iq.questrade.com/',
        }
        mock.return_value.headers = {'Content-Type': 'application/json; charset=utf-8'}

        qt_access = QTAccessService.refresh('aSBe7wAAdx88QTbwut0tiu3SYic3ox8F')

        self.assertIsInstance(qt_access, QTAccess)
        expected_access = (
            (qt_access.access_token, 'C3lTUKuNQrAAmSD/TPjuV/HI7aNrAwDp'),
            (qt_access.token_type, 'Bearer'),
            (qt_access.expires_in, 300),
            (qt_access.refresh_token, 'aSBe7wAAdx88QTbwut0tiu3SYic3ox8F'),
            (qt_access.api_server, 'https://api01.iq.questrade.com/')
        )
        for result, expected in expected_access:
            with self.subTest(result=result):
                self.assertEqual(result, expected)

    @patch('requests.get')
    def test_access_denied(self, mock):
        mock.return_value.ok = False
        mock.return_value.status_code = 400
        mock.return_value.text = 'Bad Request'
        mock.return_value.headers = {'Content-Type': 'text/html'}

        with self.assertRaises(QTError):
            QTAccessService.refresh('aSBe7wAAdx88QTbwut0tiu3SYic3ox8F')
