#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: fetcher.py
@Time: 2023/2/2-21:23
@Author: Li Dongchao
@Desc: 从网上资源抓取代理ip信息
"""

import requests

from app.utils import UACreator, logger


class Fetcher(object):

    def __init__(self):
        self.uac = UACreator()
        self.header = {"user-agent": self.uac.get()}

    def geonode(self):
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
            logger.info(f"Fetch proxy number: {len(data.get('data'))}")
            print(data.get("data"))
        else:
            logger.error("Fetch error from geonode, please check.")


if __name__ == '__main__':
    f = Fetcher()
    f.geonode()
