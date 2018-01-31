from allcoin.helper import AllCoinHelper
from common.order import Order
from constants import Constants


class AllCoinOrder(Order):
    def __init__(self, order_dict=None, symbol='oc_btc', order_redis_dict=None):
        if order_dict is not None:
            super(AllCoinOrder, self).__init__(
                exchange=Constants.EXCHANGE_NAME_ALL_COIN,
                order_id=str(order_dict['order_id']),
                order_type=AllCoinHelper.get_order_type(order_dict['type']),
                symbol=order_dict['symbol'],
                price=order_dict['price'],
                avg_price=order_dict['avg_price'],
                quantity=order_dict['amount'],
                filled_quantity=order_dict['deal_amount'],
                status=AllCoinHelper.get_status(order_dict['status'])
            )
        elif order_redis_dict is not None:
            temp_dict = {}
            for k in order_redis_dict:
                temp_dict[k.decode()] = order_redis_dict[k].decode()

            super(AllCoinOrder, self).__init__(
                exchange=Constants.EXCHANGE_NAME_ALL_COIN,
                order_id=temp_dict['order_id'],
                order_type=int(temp_dict['order_type']),
                symbol=symbol,
                price=float(temp_dict['order_price']),
                avg_price=float(temp_dict['avg_price']),
                quantity=float(temp_dict['quantity']),
                filled_quantity=float(temp_dict['filled_quantity']),
                status=int(temp_dict['status'])
            )
