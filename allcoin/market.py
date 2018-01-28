#!/usr/bin/python
# -*- coding: utf-8 -*-
from utils import http_get


class AllCoinMarket(object):
    DEPTH_RESOURCE = "/api/v1/depth"

    def __init__(self, url):
        # type: (str) -> None
        self.__url = url

    def depth(self, symbol):
        # type: (str) -> dict
        """

        :param symbol:
        :return:
        {
            'bids': [
                # [bid_price, bid_volume]
                # [float, float]
                [0.010104, 1129.16], # bid_1
                [0.010103, 1000.0], # bid_2
                [0.010102, 1000.0], # bid_3
            ],
            'asks': [
                # [ask_price, ack_volume]
                # [float, float]
                [0.0102, 10000.0], # ask_1
                [0.0106, 2799.02], # ask_2
                [0.010694, 1000.0] # ask_3
            ],
            'rawBids': None,
            'rawAsks': None,
            'id': 0,
            'seq': 0
        }
        """
        params = 'symbol=%(symbol)s' % {'symbol': symbol}
        return http_get(self.__url + AllCoinMarket.DEPTH_RESOURCE + '?' + params, False)

    def spc_qtum_bids(self):
        # type: () -> list
        """

        :return:
            [
                # [bid_price, bid_volume]
                # [float, float]
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
                # [float, float]
                [0.0109, 7690.0], # ask_1
                [0.011, 9590.0], # ask_2
                [0.01112, 147.0] # ask_3
            ]
        """
        return self.depth('oc_btc')['asks']
