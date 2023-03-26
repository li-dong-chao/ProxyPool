#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: fetcher.py
@Time: 2023/2/2-21:23
@Author: Li Dongchao
@Desc: 从网上资源抓取代理ip信息
"""

import requests

from app.utils import logger
from app.schemas.proxy import Proxy
from app.fetcher.base import BaseFetcher


class Fetcher(object):
    """
    从网上的各大免费代理网站抓取代理IP

    """

    def __init__(self):
        self.fetcher_list = BaseFetcher.check()

    def get(self):
        logger.info("开始抓取代理")
        """返回一个抓取到的代理"""
        for fetcher_class in self.fetcher_list:
            logger.info(f"{fetcher_class} start")
            try:
                for p in fetcher_class().fetch():
                    if isinstance(p, Proxy):  # 只有是Proxy类型的才返回，返回不是Proxy类型，直接跳过
                        yield p
                    else:
                        break
            except requests.RequestException as e:
                logger.error(f"{fetcher_class}执行异常，请检查: {e}")


fetcher = Fetcher()


if __name__ == '__main__':
    for x in fetcher.get():
        print(x)
