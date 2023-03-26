#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: ip3366.py
@Time: 2023/3/26-8:30
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


class Ip3366(BaseFetcher):

    def fetch(self) -> Proxy:
        for t in range(2):
            for page in range(5):
                url = f"http://www.ip3366.net/free/?stype={t+1}&page={page+1}"
                resp = requests.get(url, headers=self.header, timeout=10)
                if resp.status_code == 200:
                    tree = etree.HTML(resp.content)
                    trs = tree.xpath('.//table//tr')
                    for tr in trs[1:]:
                        ip = "".join(tr.xpath("./td[1]/text()")).strip()
                        port = "".join(tr.xpath("./td[2]/text()")).strip()
                        protocol = "".join(tr.xpath("./td[4]/text()")).strip()
                        try:
                            p = Proxy(ip=ip, port=port, protocol=protocol)
                            yield p
                        except ValidationError as e:
                            self.logger.warning(f"代理格式错误: {e}")
                else:
                    self.logger.warning(f"[{url}] 请求结果非200")
                time.sleep(random.random() * 10)


if __name__ == '__main__':
    for x in Ip3366().fetch():
        print(x)