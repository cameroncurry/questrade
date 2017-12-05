#
# Copyright Cameron Curry (c) 2017
#
from enum import Enum

from ..common import cast, qt_str


class QTBalance:

    class BalanceType(Enum):
        PER_CURRENCY = 'perCurrencyBalances'
        COMBINED = 'combinedBalances'
        SOD_PER_CURRENCY = 'sodPerCurrencyBalances'
        SOD_COMBINED = 'sodCombinedBalances'

    def __init__(self, balance_type=None, currency=None, cash=None, market_value=None,
                 total_equity=None, buying_power=None, maintenance_excess=None, is_real_time=None):
        self._balance_type = balance_type
        self._currency = currency
        self._cash = cash
        self._market_value = market_value
        self._total_equity = total_equity
        self._buying_power = buying_power
        self._maintenance_excess = maintenance_excess
        self._is_real_time = is_real_time

    @property
    def balance_type(self):
        return self._balance_type

    @property
    def currency(self):
        return self._currency

    @property
    def cash(self):
        return self._cash

    @property
    def market_value(self):
        return self._market_value

    @property
    def total_equity(self):
        return self._total_equity

    @property
    def buying_power(self):
        return self._buying_power

    @property
    def maintenance_excess(self):
        return self._maintenance_excess

    @property
    def is_real_time(self):
        return self._is_real_time

    def __str__(self):
        return qt_str(self)

    @classmethod
    def from_json(cls, balance_type, json):
        return cls(balance_type=balance_type,
                   currency=json.get('currency'),
                   cash=cast(json.get('cash'), float),
                   market_value=cast(json.get('marketValue'), float),
                   total_equity=cast(json.get('totalEquity'), float),
                   buying_power=cast(json.get('buyingPower'), float),
                   maintenance_excess=cast(json.get('maintenanceExcess'), float),
                   is_real_time=cast(json.get('isRealTime'), bool))
