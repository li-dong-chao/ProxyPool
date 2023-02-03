#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: redis_client.py
@Time: 2023/2/3-13:48
@Author: Li Dongchao
@Desc: redis客户端
@release: 
"""

from redis import Redis

from app.db.pool import redis_pool
from app.schemas.proxy import Proxy
from app.config import setting


class RedisClient(object):

    def __init__(self):
        self.key = setting.key_name
        self.redis = Redis(connection_pool=redis_pool, decode_responses=False)

    def put(self, proxy: Proxy, score: str = setting.score_init):
        """
        新增一个代理，并给其分数初始化
        :param proxy: 代理
        :param score: 分数
        :return:
        """
        self.redis.hsetnx(self.key, proxy.string(), score)

    def get(self, proxy: Proxy):
        """
        获取指定代理的分数信息
        :param proxy: 代理
        :return:
        """
        return self.redis.hget(self.key, proxy.string())

    def decrease(self, proxy: Proxy):
        """
        代理分数减一
        :param proxy: 代理
        :return:
        """
        self.redis.hincrby(self.key, proxy.string(), amount=-1)

    def reset(self, proxy: Proxy, score: str = setting.score_init):
        """
        重置代理的分数为初始分数
        :param proxy: 代理
        :param score: 初始分数
        :return:
        """
        if self.redis.hexists(self.key, proxy.string()):
            self.redis.hset(self.key, proxy.string(), score)
        else:
            raise KeyError(f"代理{proxy}不存在，无法重置")

    def increase(self, proxy: Proxy):
        """
        代理分数加一
        :param proxy: 代理
        :return:
        """
        self.redis.hincrby(self.key, proxy.string(), amount=1)


if __name__ == '__main__':
    rc = RedisClient()
    p = Proxy(ip="127.0.0.1", port=8080, protocol="http")
    rc.put(p)
    print(rc.get(p))
    rc.increase(p)
    print(rc.get(p))
    rc.reset(p)
    print(rc.get(p))
