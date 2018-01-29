from constants import Constants


class BitZHelper(object):
    @staticmethod
    def get_order_type(order_type: str) -> int:
        if order_type in Constants.BIT_Z_ORDER_TYPES:
            return Constants.BIT_Z_ORDER_TYPES[order_type]
        return Constants.ORDER_TYPE_BUY

    @staticmethod
    def get_response_order_type(order_type: str) -> int:
        if order_type in Constants.BIT_Z_RESPONSE_ORDER_TYPES:
            return Constants.BIT_Z_RESPONSE_ORDER_TYPES[order_type]
        return Constants.ORDER_TYPE_BUY

    @staticmethod
    def get_response_status(status: str, quantity: float, filled_quantity: float) -> int:
        if status == '0':
            return Constants.ORDER_STATUS_FILLED
        if abs(quantity - filled_quantity) < 0.000000001:
            return Constants.ORDER_STATUS_FILLED
        if filled_quantity < 0.000000001:
            return Constants.ORDER_STATUS_NEW
        return Constants.ORDER_STATUS_PARTIALLY_FILLED
