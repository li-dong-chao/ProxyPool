#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: kuaidaili.py
@Time: 2023/3/25-21:31
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


class KuaiDaiLi(BaseFetcher):

    def fetch(self) -> Proxy:
        for x in ["inha", "intr"]:
            for y in range(5):
                url = f"https://www.kuaidaili.com/free/{x}/{y+1}/"
                resp = requests.get(url, headers=self.header, verify=False, timeout=10)
                if resp.status_code == 200:
                    tree = etree.HTML(resp.content)
                    proxy_list = tree.xpath('.//table//tr')
                    time.sleep(1)  # 必须sleep 不然第二条请求不到数据
                    for tr in proxy_list[1:]:
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
                time.sleep(random.random() * 5)


if __name__ == '__main__':
    for xx in KuaiDaiLi().fetch():
        print(xx)
