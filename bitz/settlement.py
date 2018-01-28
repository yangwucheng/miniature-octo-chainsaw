from settlement.fee import FeeType
from settlement.settlement import Settlement


class BitZSettlement(Settlement):
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

        if sell_fee_dict['min_price'] <= price <= sell_fee_dict['max_price'] and amount >= sell_fee_dict[
            'min_quantity']:
            return True
        return False

    def get_buy_fee_dicts(self):
        return {
            'oc_btc': {
                'fee_type': FeeType.FLOAT,
                'amount': 0.001,
                'min_fee': 0.0,
                'max_fee': 9999999.0,
                'min_price': 0.0,
                'max_price': 9999999.0,
                'min_quantity': 100.00,
                'max_quantity': 500000000.00
            }
        }

    def get_default_buy_fee_dict(self):
        return {
            'fee_type': FeeType.FLOAT,
            'amount': 0.001,
            'min_fee': 0.0,
            'max_fee': 9999999.0,
            'min_price': 0.0,
            'max_price': 9999999.0,
            'min_quantity': 100.00,
            'max_quantity': 500000000.00
        }

    def get_sell_fee_dicts(self):
        return {
            'oc_btc': {
                'fee_type': FeeType.FLOAT,
                'amount': 0.001,
                'min_fee': 0.0,
                'max_fee': 9999999.0,
                'min_price': 0.0,
                'max_price': 9999999.0,
                'min_quantity': 100.00,
                'max_quantity': 500000000.00
            }
        }

    def get_default_sell_fee_dict(self):
        return {
            'fee_type': FeeType.FLOAT,
            'amount': 0.001,
            'min_fee': 0.0,
            'max_fee': 9999999.0,
            'min_price': 0.0,
            'max_price': 9999999.0,
            'min_quantity': 100.00,
            'max_quantity': 500000000.00
        }

    def get_withdraw_dicts(self):
        return {
            'btc': {
                'fee_type': FeeType.FLOAT,
                'amount': 0.005,
                'extra_fee': 0.0005,
                'min_fee': 0.0,
                'max_fee': 9999999.00,
                'min_amount': 0.01,
                'max_amount': 10.00,
                'daily_quota': 9999999.00
            },
        }

    def get_default_withdraw_dict(self):
        return {
            'fee_type': FeeType.FLOAT,
            'amount': 0.005,
            'extra_fee': 0.0005,
            'min_fee': 0.0,
            'max_fee': 9999999.00,
            'min_amount': 0.01,
            'max_amount': 10.00,
            'daily_quota': 9999999.00
        }
