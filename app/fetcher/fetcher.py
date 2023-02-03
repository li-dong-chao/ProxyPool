#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: fetcher.py
@Time: 2023/2/2-21:23
@Author: Li Dongchao
@Desc: 从网上资源抓取代理ip信息
"""

import requests
from pydantic import ValidationError

from app.utils import UACreator, logger
from app.schemas.proxy import Proxy


class Fetcher(object):

    def __init__(self):
        self.uac = UACreator()
        self.header = {"user-agent": self.uac.get()}

    def geonode(self):
        proxies = []
        url = ("https://proxylist.geonode.com/api/proxy-list?"
               "limit=500&"
               "page=1&"
               "sort_by=lastChecked&"
               "sort_type=desc&"
               "country=CN&"
               "protocols=http%2Chttps")
        resp = requests.get(url, headers=self.header)
        if resp.status_code == 200:
            data = resp.json()
            for item in data.get("data"):
                try:
                    p = Proxy(ip=item.get("ip"), port=item.get("port"), protocol=item.get("protocols")[0])
                    proxies.append(p)
                except ValidationError as e:
                    logger.warning(f"代理格式错误: {e}")
        else:
            logger.error("Fetch error from geonode, please check.")
        logger.info(f"成功抓到代理{len(proxies)}条！")
        return proxies


if __name__ == '__main__':
    f = Fetcher()
    print(f.geonode())
