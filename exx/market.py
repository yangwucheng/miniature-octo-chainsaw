#!/usr/bin/python
# -*- coding: utf-8 -*-
from utils import http_get


class ExxMarket(object):
    DEPTH_RESOURCE = "/data/v1/depth"

    def __init__(self, url):
        self.__url = url

    # 获取exx现货市场深度信息
    def depth(self, currency):
        # type: (str) -> dict
        """

        :param currency: bcc_btc, spc_qtum
        :return: dict
            {
                'timestamp': 1516520422,
                'asks': [
                    # [sell_price, sell_quantity] [str, str]
                    ['0.008600', '51200.00'], # ask_3
                    ['0.008500', '1187.62'], # ask_2
                    ['0.008479', '4234.88'] # ask_1
                ],
                'bids': [
                    # [buy_price, buy_quantity] [str, str]
                    ['0.008200', '3508.67'], # bid_1
                    ['0.008125', '6606.25'], # bid_2
                    ['0.008124', '30000.00'] # bid_3
                ]
            }
        """
        params = 'currency=%(currency)s' % {'currency': currency}
        return http_get(self.__url + ExxMarket.DEPTH_RESOURCE + '?' + params)

    def spc_qtum_depth(self):
        # type: () -> dict
        """

        :return: spc_qtum depth
        """
        return self.depth('spc_qtum')

    def spc_qtum_bids(self):
        # type: () -> list(list)
        """

        :return: spc_qtum bids
            [
                # [buy_price, buy_quantity]
                ['0.008200', '3508.67'], # bid_1
                ['0.008125', '6606.25'], # bid_2
                ['0.008124', '30000.00'] # bid_3
            ]
        """
        return self.spc_qtum_depth()['bids']

    def spc_qtum_asks(self):
        # type: () -> list(list)
        """

        :return: spc_qtum asks
            [
                # [sell_price, sell_quantity]
                ['0.008600', '51200.00'], # ask_3
                ['0.008500', '1187.62'], # ask_2
                ['0.008479', '4234.88'] # ask_1
            ]
        """
        return self.spc_qtum_depth()['asks']
