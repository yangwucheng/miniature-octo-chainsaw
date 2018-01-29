class Constants(object):
    ORDER_STATUS_NEW = 0
    ORDER_STATUS_PARTIALLY_FILLED = 1
    ORDER_STATUS_FILLED = 2
    ORDER_STATUS_CANCELLED = 3

    ORDER_TYPE_BUY = 0
    ORDER_TYPE_SELL = 1

    ALL_COIN_ORDER_TYPES = {
        'buy': ORDER_TYPE_BUY,
        'sell': ORDER_TYPE_SELL
    }

    BIT_Z_ORDER_TYPES = {
        'in': ORDER_TYPE_BUY,
        'out': ORDER_TYPE_SELL
    }

    BIT_Z_RESPONSE_ORDER_TYPES = {
        'sale': ORDER_TYPE_SELL
    }

    EXCHANGE_NAME_ALL_COIN = 'allCoin'
    EXCHANGE_NAME_BIT_Z = 'bitZ'

    REDIS_KEY_ALL_COIN_POSITIONS = 'allCoinPositions'
    REDIS_KEY_ALL_COIN_OPEN_ORDER_IDS_PREFIX = 'allCoinOpenOrderIds'
    REDIS_KEY_ALL_COIN_CANCELLED_ORDER_IDS_PREFIX = 'allCoinCancelledOrderIds'
    REDIS_KEY_ALL_COIN_CLOSED_ORDER_IDS_PREFIX = 'allCoinClosedOrderIds'
    REDIS_KEY_ALL_COIN_ORDER_PREFIX = 'allCoinOrder'
    REDIS_KEY_ALL_COIN_TRADE_PAIRS = 'allCoinTradePairs'

    REDIS_KEY_BIT_Z_POSITIONS = 'bitZPositions'
    REDIS_KEY_BIT_Z_OPEN_ORDER_IDS_PREFIX = 'bitZOpenOrderIds'
    REDIS_KEY_BIT_Z_CANCELLED_ORDER_IDS_PREFIX = 'bitZCancelledOrderIds'
    REDIS_KEY_BIT_Z_CLOSED_ORDER_IDS_PREFIX = 'bitZClosedOrderIds'
    REDIS_KEY_BIT_Z_ORDER_PREFIX = 'bitZOrder'
    REDIS_KEY_BIT_Z_TRADE_PAIRS = 'bitZTradePairs'

    ALL_COIN_ORDER_STATUS_NEW = 0
    ALL_COIN_ORDER_STATUS_PARTIALLY_FILLED = 1
    ALL_COIN_ORDER_STATUS_FILLED = 2
    ALL_COIN_ORDER_STATUS_CANCELLED = 10
