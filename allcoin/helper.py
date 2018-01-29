from constants import Constants


class AllCoinHelper(object):
    @staticmethod
    def get_order_type(order_type):
        if order_type in Constants.ALL_COIN_ORDER_TYPES:
            return Constants.ALL_COIN_ORDER_TYPES[order_type]
        return Constants.ORDER_TYPE_BUY

    @staticmethod
    def get_status(status):
        if status == Constants.ALL_COIN_ORDER_STATUS_NEW:
            return Constants.ORDER_STATUS_NEW

        if status == Constants.ALL_COIN_ORDER_STATUS_PARTIALLY_FILLED:
            return Constants.ORDER_STATUS_PARTIALLY_FILLED

        if status == Constants.ALL_COIN_ORDER_STATUS_FILLED:
            return Constants.ORDER_STATUS_FILLED

        return Constants.ORDER_STATUS_CANCELLED
