from allcoin.helper import AllCoinHelper
from common.order import Order
from constants import Constants


class AllCoinOrder(Order):
    def __init__(self, order_dict):
        super(AllCoinOrder, self).__init__(
            exchange=Constants.EXCHANGE_NAME_ALL_COIN,
            order_id=order_dict['order_id'],
            order_type=AllCoinHelper.get_order_type(order_dict['type']),
            symbol=order_dict['symbol'],
            price=order_dict['price'],
            avg_price=order_dict['avg_price'],
            quantity=order_dict['amount'],
            filled_quantity=order_dict['deal_amount'],
            status=AllCoinHelper.get_status(order_dict['status'])
        )
