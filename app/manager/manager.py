#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: manager.py
@Time: 2023/2/3-17:15
@Author: Li Dongchao
@Desc: 
@release: 
"""

from app.fetcher.fetcher import Fetcher
from app.validator.validator import Validator
from app.db.redis_client import RedisClient


class Manager(object):

    def __init__(self):
        self.fetcher = Fetcher()
        self.validator = Validator()
        self.redis_cli = RedisClient()

    def fetch(self):
        """
        从各个免费代理网站获取代理
        """
        proxies = self.fetcher.geonode()  # todo: 后续多个不同的免费代理网站如何进行设计？尽量设置为可插拔式
        while proxies:
            cur_proxy = proxies.pop()
            self.redis_cli.put(proxy=cur_proxy)

    def validate(self):
        """
        验证代理的有效性
        """
        self.redis_cli
