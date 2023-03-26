#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: fatezero.py
@Time: 2023/3/25-22:22
@Author: Li Dongchao
@Desc: 
"""
import json
import requests
from pydantic import ValidationError

from app.fetcher.base import BaseFetcher
from app.schemas.proxy import Proxy


class FateZero(BaseFetcher):

    def fetch(self) -> Proxy:
        url = "http://proxylist.fatezero.org/proxy.list"
        resp = requests.get(url, headers=self.header, timeout=10)
        if resp.status_code == 200:
            resp_text = resp.text
            for each in resp_text.split("\n"):
                try:
                    json_info = json.loads(each)
                except json.JSONDecodeError as _:
                    continue
                if json_info.get("country") == "CN":
                    ip = json_info.get("host", "")
                    port = json_info.get("port", "")
                    protocol = json_info.get("type", "")
                    try:
                        p = Proxy(ip=ip, port=port, protocol=protocol)
                        yield p
                    except ValidationError as e:
                        self.logger.warning(f"代理格式错误: {e}")
        else:
            self.logger.warning(f"[{url}] 请求结果非200")


if __name__ == '__main__':
    for x in FateZero().fetch():
        print(x)