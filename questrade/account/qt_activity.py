#
# Copyright Cameron Curry (c) 2017
#

from ..common import cast, cast_datetime, qt_str


class QTActivity:

    def __init__(self, trade_date=None, transaction_date=None, settlement_date=None, action=None,
                 symbol=None, symbol_id=None, description=None, currency=None, quantity=None,
                 price=None, gross_amount=None, commission=None, net_amount=None, activity_type=None):
        self._trade_date = trade_date
        self._transaction_date = transaction_date
        self._settlement_date = settlement_date
        self._action = action
        self._symbol = symbol
        self._symbol_id = symbol_id
        self._description = description
        self._currency = currency
        self._quantity = quantity
        self._price = price
        self._gross_amount = gross_amount
        self._commission = commission
        self._net_amount = net_amount
        self._activity_type = activity_type

    @property
    def trade_date(self):
        return self._trade_date

    @property
    def transaction_date(self):
        return self._transaction_date

    @property
    def settlement_date(self):
        return self._settlement_date

    @property
    def action(self):
        return self._action

    @property
    def symbol(self):
        return self._symbol

    @property
    def symbol_id(self):
        return self._symbol_id

    @property
    def description(self):
        return self._description

    @property
    def currency(self):
        return self._currency

    @property
    def quantity(self):
        return self._quantity

    @property
    def price(self):
        return self._price

    @property
    def gross_amount(self):
        return self._gross_amount

    @property
    def commission(self):
        return self._commission

    @property
    def net_amount(self):
        return self._net_amount

    @property
    def activity_type(self):
        return self._activity_type

    def __str__(self):
        return qt_str(self)

    @classmethod
    def from_json(cls, json):
        return cls(trade_date=cast_datetime(json.get('tradeDate')),
                   transaction_date=cast_datetime(json.get('tradeDate')),
                   settlement_date=cast_datetime(json.get('settlementDate')),
                   action=json.get('action'),
                   symbol=json.get('symbol'),
                   symbol_id=cast(json.get('symbolId'), int),
                   description=json.get('description'),
                   currency=json.get('currency'),
                   quantity=cast(json.get('quantity'), int),
                   price=cast(json.get('price'), float),
                   gross_amount=cast(json.get('grossAmount'), float),
                   commission=cast(json.get('commission'), float),
                   net_amount=cast(json.get('netAmount'), float),
                   activity_type=json.get('type'))
