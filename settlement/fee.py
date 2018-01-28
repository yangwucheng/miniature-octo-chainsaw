class FeeType(object):
    FLOAT = 0
    FIXED = 1


class Fee(object):
    def __init__(self, fee_dict):
        # type: (int, float, float, float) -> None
        self.__fee_type = fee_dict['fee_type']
        self.__amount = fee_dict['amount']
        self.__min_fee = fee_dict['min_fee']
        self.__max_fee = fee_dict['max_fee']
        self.__extra_fee = 0.0
        if 'extra_fee' in fee_dict:
            self.__extra_fee = fee_dict['extra_fee']

    def calculate_fee(self, price, quantity):
        # type: (float, float) -> float
        if self.__fee_type == FeeType.FIXED:
            return self.__amount

        turnover = price * quantity
        fee = turnover * self.__amount
        if fee < self.__min_fee:
            fee = self.__min_fee

        if fee > self.__max_fee:
            fee = self.__max_fee
        return fee + self.__extra_fee
