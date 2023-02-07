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
from app.utils import logger


class Manager(object):

    def __init__(self):
        self.fetcher = Fetcher()
        self.validator = Validator()
        self.db = RedisClient()
        self.logger = logger

    def fetch(self):
        """
        从各个免费代理网站获取代理
        """
        # proxies.extend(self.fetcher.geonode())  # todo: 后续多个不同的免费代理网站如何进行设计？尽量设置为可插拔式
        proxies = self.fetcher.execute()
        while proxies:
            cur_proxy = proxies.pop()
            self.db.add(proxy=cur_proxy)

    def validate(self, proxy):
        """
        验证代理的有效性
        """
        is_valid = Validator.check_proxy(proxy)
        if is_valid:
            self.db.max(proxy)
        else:
            self.db.decrease(proxy)

    def validate_all(self):
        all_proxies = self.db.all()
        self.logger.info(f"当前数据库中有{self.db.count()}条数据，即将开始验证代理有效性...")
        for proxy in all_proxies:
            self.validate(proxy)
        self.logger.info(f"已验证{self.db.count()}条代理数据，"
                         f"其中有效代理{self.db.count_max()}条")

    def get_proxy(self):
        """
        返回一个有效代理
        :return:
        """
        return self.db.get().string()


if __name__ == '__main__':
    manager = Manager()
    manager.fetch()
    manager.validate_all()
    print(manager.db.all())
