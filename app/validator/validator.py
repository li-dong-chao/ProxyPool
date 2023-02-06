#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: validator.py
@Time: 2023/2/3-16:39
@Author: Li Dongchao
@Desc: 
@release: 
"""

import requests
from requests.exceptions import Timeout, ProxyError, RequestException

from app.utils import UACreator
from app.schemas.proxy import Proxy


# todo: 后续修改为多线程检查或协程检查

class Validator(object):

    @staticmethod
    def check_proxy(proxy: Proxy):
        test_url = "https://baidu.com"
        headers = {
            "user-agent": UACreator().get()
        }
        proxy = {
            "http": proxy.string(),
            "https": proxy.string()
        }
        try:
            resp = requests.get(
                test_url,
                proxies=proxy,
                headers=headers,
                timeout=10
            )
        except (Timeout, ProxyError, RequestException) as _:
            return False
        if resp.status_code == 200:
            if "<title>百度一下，你就知道</title>" in resp.text:
                return True
        return False


if __name__ == '__main__':
    print(Validator.check_proxy(Proxy(ip="127.0.0.1", port="8000", protocol="http")))
