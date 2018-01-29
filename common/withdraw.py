class Withdraw(object):
    def __init__(self, withdraw_dict):
        self.__min_amount = withdraw_dict['min_amount']
        self.__max_amount = withdraw_dict['max_amount']
        self.__daily_quota = withdraw_dict['daily_quota']

    def can_withdraw(self, amount):
        if self.__min_amount <= amount <= self.__max_amount and amount <= self.__daily_quota:
            return True

        return False
