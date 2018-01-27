#!/usr/bin/python
# -*- coding: utf-8 -*-
from utils import http_get


class BitZMarket(object):
    DEPTH_RESOURCE = "/api_v1/depth"

    def __init__(self, url):
        self.__url = url

    def depth(self, coin):
        params = 'coin=%(coin)s' % {'coin': coin}
        return http_get(self.__url + BitZMarket.DEPTH_RESOURCE + '?' + params)

    def oc_btc_bids(self):
        # type: () -> list
        """

        :return:
            [
                # [bid_price, bid_volume]
                ['0.00000220', '160033.0069'], # bid_1
                ['0.00000217', '1272.5387'], # bid_2
                ['0.00000216', '54.2032'] # bid_3
            ]
        """
        return self.depth('oc_btc')['data']['bids']