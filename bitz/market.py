#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from utils import http_get


class BitZMarket(object):
    DEPTH_RESOURCE = "/api_v1/depth"
    K_LINE_RESOURCE = "/api_v1/kline"

    def __init__(self, url):
        # type: (str) -> str
        self.__url = url

    def depth(self, coin):
        """

        :param coin: str
        :type coin: str
        :return:
        {
            "code": 0, // 状态码
            "msg": "Success", // 提示语
            "data": {
                "asks": [
                    ['0.00000210', '12867.7080'],
                    ['0.00000209', '123770.4725'],
                    ['0.00000208', '162688.6625']
                ], //asks 委卖单[价格, 委单量]，价格从高到低排序 [str, str]
                "bids": [
                    ['0.00000195', '893.0000'],
                    ['0.00000193', '22826.6243'],
                    ['0.00000192', '90270.4217']
                ], //bids 委买单[价格, 委单量]，价格从高到低排序 [str, str]
                "date": 1506047161 //时间戳
            }
        }
        """
        params = 'coin=%(coin)s' % {'coin': coin}
        return http_get(self.__url + BitZMarket.DEPTH_RESOURCE + '?' + params)

    def oc_btc_asks(self):
        """

        :return:
            "asks": [
                ['0.00000210', '12867.7080'], # ask_3
                ['0.00000209', '123770.4725'], # ask_2
                ['0.00000208', '162688.6625'] # ask_1
            ], //asks 委卖单[价格, 委单量]，价格从高到低排序 [str, str]
        """
        return self.depth('oc_btc')['data']['asks']

    def oc_btc_bids(self):
        # type: () -> list
        """

        :return:
            [
                # [bid_price, bid_volume] [str, str]
                ['0.00000220', '160033.0069'], # bid_1
                ['0.00000217', '1272.5387'], # bid_2
                ['0.00000216', '54.2032'] # bid_3
            ]
        """
        return self.depth('oc_btc')['data']['bids']

    def oc_btc_bid_1(self):
        # type: () -> list
        """

        :return: [str, str]
        """
        return self.oc_btc_bids()[0]

    def oc_btc_bid_1_price(self):
        # type: () -> str
        return self.oc_btc_bid_1()[0]

    def oc_btc_bid_1_volume(self):
        # type: () -> str
        return self.oc_btc_bid_1()[1]

    def k_line(self, coin, k_type):
        """

        :param coin:
        :type coin: str
        :param k_type:
        :type k_type: str, 1m, 5m, 15m, 30m, 1h, 1d
        :return:
        [[timestamp, open, high, low, close, volume]] [[int, float, float, float, float, float]]
        [
            [1517063160000, 2.24e-06, 2.24e-06, 2.24e-06, 2.24e-06, 100.0],
            [1517063220000, 2.24e-06, 2.27e-06, 2.24e-06, 2.24e-06, 1790],
            [1517063280000, 2.24e-06, 2.24e-06, 2.24e-06, 2.24e-06, 100.0]
        ]
        """
        params = 'coin=%(coin)s&type=%(type)s' % {'coin': coin, 'type': k_type}
        ret = http_get(self.__url + BitZMarket.K_LINE_RESOURCE + '?' + params)
        if 'code' in ret and ret['code'] == 0:
            return json.loads(ret['data']['datas']['data'])

    def oc_btc_1m_k_line(self):
        return self.k_line('oc_btc', '1m')

    @staticmethod
    def is_hot(k1, k2):
        TIMESTAMP = 0
        OPEN = 1
        HIGH = 2
        LOW = 3
        CLOSE = 4
        VOLUME = 5
        if k2[VOLUME] / k1[VOLUME] > 10 and k2[VOLUME] > 200000:
            return True
        return False

    @staticmethod
    def is_continue(t1, t2):
        if t2 - t1 == 60 * 1000:
            return True
        return False
