#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: geonode.py
@Time: 2023/3/25-18:10
@Author: Li Dongchao
@Desc: 
"""

import requests
from pydantic import ValidationError

from app.fetcher.base import BaseFetcher
from app.schemas.proxy import Proxy


class Geonode(BaseFetcher):

    def fetch(self) -> Proxy:
        url = ("https://proxylist.geonode.com/api/proxy-list?"
               "limit=500&"
               "page=1&"
               "sort_by=lastChecked&"
               "sort_type=desc&"
               "protocols=http%2Chttps")
        resp = requests.get(url, headers=self.header, verify=False, timeout=20)
        if resp.status_code == 200:
            data = resp.json()
            for item in data.get("data"):
                try:
                    p = Proxy(ip=item.get("ip"), port=item.get("port"), protocol=item.get("protocols")[0])
                    yield p
                except ValidationError as e:
                    self.logger.warning(f"代理格式错误: {e}")
        else:
            self.logger.error(f"[{url}] 请求结果非200")


if __name__ == '__main__':
    for x in Geonode().fetch():
        print(x)