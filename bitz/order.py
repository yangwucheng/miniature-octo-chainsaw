from bitz.helper import BitZHelper
from common.order import Order
from constants import Constants


class BitZOrder(Order):
    def __init__(self, order_dict=None, symbol='oc_btc', order_redis_dict=None):
        # {
        #         'id': '85493197',
        #         'price': '0.00000214',
        #         'number': '10000.0000',
        #         'numberover': '10000.0000',
        #         'flag': 'sale',
        #         'status': '0',
        #         'datetime': '2018-01-28 09:30:42'
        #     }
        if order_dict is not None:
            super(BitZOrder, self).__init__(
                exchange=Constants.EXCHANGE_NAME_BIT_Z,
                order_id=order_dict['id'],
                order_type=BitZHelper.get_response_order_type(order_dict['flag']),
                symbol=symbol,
                price=float(order_dict['price']),
                avg_price=float(order_dict['price']),
                quantity=float(order_dict['number']),
                filled_quantity=float(order_dict['number']) - float(order_dict['numberover']),
                status=BitZHelper.get_response_status(order_dict['status'], float(order_dict['number']),
                                                      float(order_dict['number']) - float(order_dict['numberover']))
            )
        elif order_redis_dict is not None:
            temp_dict = {}
            for k in order_redis_dict:
                temp_dict[k.decode()] = order_redis_dict[k].decode()

            super(BitZOrder, self).__init__(
                exchange=Constants.EXCHANGE_NAME_BIT_Z,
                order_id=temp_dict['order_id'],
                order_type=int(temp_dict['order_type']),
                symbol=symbol,
                price=float(temp_dict['order_price']),
                avg_price=float(temp_dict['order_price']),
                quantity=float(temp_dict['quantity']),
                filled_quantity=float(temp_dict['filled_quantity']),
                status=int(temp_dict['status'])
            )
