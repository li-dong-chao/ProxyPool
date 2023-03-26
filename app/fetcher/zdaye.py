#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: zdaye.py
@Time: 2023/3/25-19:22
@Author: Li Dongchao
@Desc: 
"""
import time
from lxml import etree
import requests
import random
from datetime import datetime
from pydantic import ValidationError

from app.fetcher.base import BaseFetcher
from app.schemas.proxy import Proxy


class ZDaYe(BaseFetcher):

    def fetch(self) -> Proxy:
        start_url = "https://www.zdaye.com/dayProxy.html"
        resp = requests.get(start_url, headers=self.header, verify=False)
        if resp.status_code == 200:
            html_tree = etree.HTML(resp.content)
            latest_page_time = html_tree.xpath("//span[@class='thread_time_info']/text()")[0].strip()
            interval = datetime.now() - datetime.strptime(latest_page_time, "%Y/%m/%d %H:%M:%S")
            if interval.seconds < 24 * 60 * 60:  # 只采集近一天的更新
                target_url = ("https://www.zdaye.com/" +
                              html_tree.xpath("//h3[@class='thread_title']/a/@href")[0].strip())
                while target_url:
                    resp = requests.get(target_url, headers=self.header, verify=False)
                    if resp.status_code == 200:
                        _tree = etree.HTML(resp.content)
                        for tr in _tree.xpath("//table//tr"):
                            ip = "".join(tr.xpath("./td[1]/text()")).strip()
                            port = "".join(tr.xpath("./td[2]/text()")).strip()
                            protocol = "".join(tr.xpath("./td[3]/text()")).strip()
                            try:
                                p = Proxy(ip=ip, port=port, protocol=protocol)
                                yield p
                            except ValidationError as e:
                                self.logger.warning(f"代理格式错误: {e}")
                        next_page = _tree.xpath("//div[@class='page']/a[@title='下一页']/@href")
                        target_url = "https://www.zdaye.com/" + next_page[0].strip() if next_page else False
                    else:
                        self.logger.warning(f"[{target_url}] 请求结果非200")
                    time.sleep(random.random() * 10)
        else:
            self.logger.warning(f"[{start_url}] 请求结果非200")


if __name__ == '__main__':
    for x in ZDaYe().fetch():
        print(x)
