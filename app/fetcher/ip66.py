#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: ip66.py
@Time: 2023/3/25-20:07
@Author: Li Dongchao
@Desc: 
"""
import time
import random
import requests
from lxml import etree
from pydantic import ValidationError

from app.fetcher.base import BaseFetcher
from app.schemas.proxy import Proxy


class IP66(BaseFetcher):

    def fetch(self) -> Proxy:
        for page in range(10):
            url = f"http://www.66ip.cn/{page + 1}.html"
            resp = requests.get(url, headers=self.header, timeout=10)
            if resp.status_code == 200:
                resp = etree.HTML(resp.content)
                for i, tr in enumerate(resp.xpath("(//table)[3]//tr")):
                    if i > 0:
                        ip = "".join(tr.xpath("./td[1]/text()")).strip()
                        port = "".join(tr.xpath("./td[2]/text()")).strip()
                        protocol = "http"
                        try:
                            p = Proxy(ip=ip, port=port, protocol=protocol)
                            yield p
                        except ValidationError as e:
                            self.logger.warning(f"代理格式错误: {e}")
            else:
                self.logger.warning(f"[{url}] 请求结果非200")
            time.sleep(random.random() * 10)


if __name__ == '__main__':
    for x in IP66().fetch():
        print(x)
