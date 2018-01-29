from bitz.helper import BitZHelper
from common.order import Order
from constants import Constants


class BitZOrder(Order):
    def __init__(self, order_dict, symbol):
        # {
        #         'id': '85493197',
        #         'price': '0.00000214',
        #         'number': '10000.0000',
        #         'numberover': '10000.0000',
        #         'flag': 'sale',
        #         'status': '0',
        #         'datetime': '2018-01-28 09:30:42'
        #     }

        super(BitZOrder, self).__init__(
            exchange=Constants.EXCHANGE_NAME_BIT_Z,
            order_id=order_dict['id'],
            order_type=BitZHelper.get_repsonse_order_type(order_dict['flag']),
            symbol=symbol,
            price=order_dict['price'],
            avg_price=order_dict['price'],
            quantity=order_dict['number'],
            filled_quantity=order_dict['numberover'],
            status=BitZHelper.get_response_status(order_dict['status'], order_dict['number'], order_dict['numberover'])
        )
