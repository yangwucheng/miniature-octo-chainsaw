#!/usr/bin/python
# -*- coding: utf-8 -*-
from utils import http_get


class AllCoinMarket(object):
    DEPTH_RESOURCE = "/api/v1/depth"

    def __init__(self, url):
        self.__url = url

    # 获取exx现货市场深度信息
    def depth(self, symbol):
        # type: (str) -> dict
        params = 'symbol=%(symbol)s' % {'symbol': symbol}
        return http_get(self.__url + AllCoinMarket.DEPTH_RESOURCE + '?' + params, False)

    def spc_qtum_bids(self):
        # type: () -> list
        """

        :return:
            [
                # [bid_price, bid_volume]
                [0.0095, 5444.8], # bid_1
                [0.009, 2275.4], # bid_2
                [0.00867, 3282.35] # bid_3
            ]
        """
        return self.depth('spc_qtum')['bids']

    def oc_btc_asks(self):
        # type: () -> list
        """

        :return:
            [
                # [ask_price, ack_volume]
                [0.0109, 7690.0], # ask_1
		        [0.011, 9590.0], # ask_2
		        [0.01112, 147.0] # ask_3
            ]
        """
        return self.depth('oc_btc')['asks']
