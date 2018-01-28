from settlement.fee import FeeType
from settlement.settlement import Settlement


class AllCoinSettlement(Settlement):
    def get_min_buy_quantity(self, symbol):
        # type: (str) -> float
        buy_fee_dict = self.get_default_buy_fee_dict()
        if symbol.lower() in self.get_buy_fee_dicts():
            buy_fee_dict = self.get_buy_fee_dicts()[symbol.lower()]

        return buy_fee_dict['min_quantity']

    def get_min_sell_quantity(self, symbol):
        # type: (str) -> float
        sell_fee_dict = self.get_default_sell_fee_dict()
        if symbol.lower() in self.get_sell_fee_dicts():
            sell_fee_dict = self.get_sell_fee_dicts()[symbol.lower()]

        return sell_fee_dict['min_quantity']

    def is_valid_buy_order(self, symbol, price, amount):
        # type: (str, float, float) -> bool
        buy_fee_dict = self.get_default_buy_fee_dict()
        if symbol.lower() in self.get_buy_fee_dicts():
            buy_fee_dict = self.get_buy_fee_dicts()[symbol.lower()]

        if buy_fee_dict['min_price'] <= price <= buy_fee_dict['max_price'] and amount >= buy_fee_dict['min_quantity']:
            return True
        return False

    def is_valid_sell_order(self, symbol, price, amount):
        # type: (str, float, float) -> bool
        sell_fee_dict = self.get_default_sell_fee_dict()
        if symbol.lower() in self.get_sell_fee_dicts():
            sell_fee_dict = self.get_sell_fee_dicts()[symbol.lower()]

        if sell_fee_dict['min_price'] <= price <= sell_fee_dict['max_price'] and amount >= sell_fee_dict['min_quantity']:
            return True
        return False

    def get_buy_fee_dicts(self):
        return {
            'spc_qtum': {
                'fee_type': FeeType.FIXED,
                'amount': 0.0,
                'min_fee': 0.0,
                'max_fee': 0.0,
                'min_price': 0.000800,
                'max_price': 0.800000,
                'min_quantity': 2.00
            },
            'oc_btc': {
                'fee_type': FeeType.FIXED,
                'amount': 0.0,
                'min_fee': 0.0,
                'max_fee': 0.0,
                'min_price': 0.00000021,
                'max_price': 0.00021400,
                'min_quantity': 40.00
            }
        }

    def get_default_buy_fee_dict(self):
        return {
            'fee_type': FeeType.FIXED,
            'amount': 0.0,
            'min_fee': 0.0,
            'max_fee': 0.0,
            'min_price': 0.00000001,
            'max_price': 1.00000000,
            'min_quantity': 100.00
        }

    def get_sell_fee_dicts(self):
        return {
            'spc_qtum': {
                'fee_type': FeeType.FLOAT,
                'amount': 0.002,
                'min_fee': 0.0,
                'max_fee': 9999999.0,
                'min_price': 0.000800,
                'max_price': 0.800000,
                'min_quantity': 2.00
            },
            'oc_btc': {
                'fee_type': FeeType.FLOAT,
                'amount': 0.002,
                'min_fee': 0.0,
                'max_fee': 9999999.0,
                'min_price': 0.00000021,
                'max_price': 0.00021400,
                'min_quantity': 40.00
            }
        }

    def get_default_sell_fee_dict(self):
        return {
            'fee_type': FeeType.FLOAT,
            'amount': 0.002,
            'min_fee': 0.0,
            'max_fee': 9999999.0,
            'min_price': 0.00000001,
            'max_price': 1.00000000,
            'min_quantity': 100.00
        }

    def get_withdraw_dicts(self):
        return {
            'qtum': {
                'fee_type': FeeType.FLOAT,
                'amount': 0.002,
                'min_fee': 0.002,
                'max_fee': 9999999.0,
                'min_amount': 0.2,
                'max_amount': 1000.00,
                'daily_quota': 1000.00
            },
            'btc': {
                'fee_type': FeeType.FLOAT,
                'amount': 0.002,
                'min_fee': 0.0015,
                'max_fee': 9999999.00,
                'min_amount': 0.01,
                'max_amount': 50.00,
                'daily_quota': 50.00
            },
            'oc': {
                'fee_type': FeeType.FLOAT,
                'amount': 0.002,
                'min_fee': 320,
                'max_fee': 9999999.00,
                'min_amount': 800.00,
                'max_amount': 4000000.00,
                'daily_quota': 4000000.00
            },
            'spc': {
                'fee_type': FeeType.FLOAT,
                'amount': 0.002,
                'min_fee': 25,
                'max_fee': 9999999.00,
                'min_amount': 35.00,
                'max_amount': 175000.00,
                'daily_quota': 175000.00
            }
        }

    def get_default_withdraw_dict(self):
        return {
            'fee_type': FeeType.FLOAT,
            'amount': 0.002,
            'min_fee': 25,
            'max_fee': 9999999.00,
            'min_amount': 35.00,
            'max_amount': 175000.00,
            'daily_quota': 175000.00
        }
