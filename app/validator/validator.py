#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: validator.py
@Time: 2023/2/3-16:39
@Author: Li Dongchao
@Desc: 通过测试是否能成功请求百度，来对代理的有效性进行验证
@release: 
"""

import requests
from requests.exceptions import Timeout, ProxyError, RequestException

from app.utils import UACreator
from app.schemas.proxy import Proxy


class Validator(object):

    @staticmethod
    def check_proxy(proxy: Proxy):
        """通过测试是否能成功请求百度，来对代理的有效性进行验证"""
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
                timeout=5
            )
        except (Timeout, ProxyError, RequestException) as _:
            return False
        if resp.status_code == 200:
            if "<title>百度一下，你就知道</title>" in resp.text:
                return True
        return False


if __name__ == '__main__':
    print(Validator.check_proxy(Proxy(ip="127.0.0.1", port="8000", protocol="http")))
