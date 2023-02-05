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
import bs4

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
            logger.info(f"抓到代理{len(proxies)}条！")
        else:
            logger.error("Fetch error from geonode, please check.")
        return proxies

    def jiangxianli(self):
        proxies = []
        url = "https://ip.jiangxianli.com/"
        resp = requests.get(url, headers=self.header, verify=False)
        if resp.status_code == 200:
            soup = bs4.BeautifulSoup(resp.text, "html.parser")
            trs = soup.find_all("tr")
            for tr in trs[1:]:
                try:
                    tds = tr.find_all("td")
                    if len(tds) > 4:
                        ip = tds[0].text
                        port = tds[1].text
                        protocol = tds[3].text.lower()
                        p = Proxy(ip=ip, port=port, protocol=protocol)
                        proxies.append(p)
                except ValidationError as e:
                    logger.warning(f"代理格式错误: {e}")
            logger.info(f"抓到代理{len(proxies)}条！")
        else:
            logger.error("Fetch error from free_proxy, please check.")
        return proxies


if __name__ == '__main__':
    f = Fetcher()
    print(f.jiangxianli())
