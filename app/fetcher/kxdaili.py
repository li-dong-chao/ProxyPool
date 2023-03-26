#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: kxdaili.py
@Time: 2023/3/25-21:06
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


class KXDaiLi(BaseFetcher):

    def fetch(self) -> Proxy:
        for x in range(2):
            for y in range(5):
                target_url = f"http://www.kxdaili.com/dailiip/{x+1}/{y+1}.html"
                resp = requests.get(target_url, headers=self.header, timeout=5)
                if resp.status_code == 200:
                    tree = etree.HTML(resp.content)
                    for tr in tree.xpath("//table[@class='active']//tr")[1:]:
                        ip = "".join(tr.xpath('./td[1]/text()')).strip()
                        port = "".join(tr.xpath('./td[2]/text()')).strip()
                        protocol = "".join(tr.xpath('./td[4]/text()')).strip().split(",")[-1]
                        try:
                            p = Proxy(ip=ip, port=port, protocol=protocol)
                            yield p
                        except ValidationError as e:
                            self.logger.warning(f"代理格式错误: {e}")
                else:
                    self.logger.warning(f"[{target_url}] 请求结果非200")
                time.sleep(random.random() * 10)


if __name__ == '__main__':
    for xx in KXDaiLi().fetch():
        print(xx)
