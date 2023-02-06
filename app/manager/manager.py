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
        self.redis_cli = RedisClient()
        self.logger = logger

    def fetch(self):
        """
        从各个免费代理网站获取代理
        """
        proxies = []
        # proxies.extend(self.fetcher.geonode())  # todo: 后续多个不同的免费代理网站如何进行设计？尽量设置为可插拔式
        proxies.extend(self.fetcher.jiangxianli())
        while proxies:
            cur_proxy = proxies.pop()
            self.redis_cli.put(proxy=cur_proxy)

    def validate(self, proxy):
        """
        验证代理的有效性
        """
        print(proxy)
        is_valid = Validator.check_proxy(proxy)
        if is_valid:
            self.redis_cli.reset(proxy)
            self.logger.info(f"[{proxy}] 验证通过，当前分数: {self.redis_cli.get_score(proxy)}")
        else:
            self.redis_cli.decrease(proxy)
            if self.redis_cli.exist_proxy(proxy):
                self.logger.info(f"[{proxy}] 验证失败，当前分数: {self.redis_cli.get_score(proxy)}")
            else:
                self.logger.info(f"[{proxy}] 验证失败, 分数归零，已经清除")

    def validate_all(self):
        all_proxies = self.redis_cli.all_proxy()
        self.logger.info(f"当前数据库中有{self.redis_cli.count_all_proxy()}条数据，即将开始验证代理有效性...")
        for proxy in all_proxies:
            self.validate(proxy)
        self.logger.info(f"已验证{self.redis_cli.count_all_proxy()}条代理数据，"
                         f"其中有效代理{self.redis_cli.count_valid_proxy()}条")

    def get_proxy(self):
        """
        返回一个有效代理
        :return:
        """
        return self.redis_cli.a_valid_proxy().string()


if __name__ == '__main__':
    manager = Manager()
    manager.fetch()
    manager.validate_all()
    print(manager.redis_cli.all_valid_proxy())
