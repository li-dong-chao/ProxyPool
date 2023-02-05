#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: redis_client.py
@Time: 2023/2/3-13:48
@Author: Li Dongchao
@Desc: redis客户端
@release: 
"""

from redis import StrictRedis

from app.db.pool import redis_pool
from app.schemas.proxy import Proxy
from app.config import setting


class RedisClient(object):

    def __init__(self):
        self.all_proxy_key = "all_proxy"
        self.valid_proxy_key = "valid_proxy"
        self.redis = StrictRedis(connection_pool=redis_pool)

    def put(self, proxy: Proxy, score: str = setting.score_init):
        """
        新增一个代理，并给其分数初始化
        :param proxy: 代理
        :param score: 分数
        :return:
        """
        self.redis.hsetnx(self.all_proxy_key, proxy.string(), score)

    def get(self, proxy: Proxy):
        """
        获取指定代理的分数信息
        :param proxy: 代理
        :return:
        """
        return int(self.redis.hget(self.all_proxy_key, proxy.string()))

    def exist_proxy(self, proxy: Proxy):
        return self.redis.hexists(self.all_proxy_key, proxy.string())

    def remove(self, proxy: Proxy):
        """
        从数据库中删除代理
        :param proxy: 代理
        :return:
        """
        self.redis.hdel(self.all_proxy_key, proxy.string())

    def decrease(self, proxy: Proxy):
        """
        代理分数减一
        :param proxy: 代理
        :return:
        """
        self.redis.hincrby(self.all_proxy_key, proxy.string(), amount=-1)
        if self.get(proxy) <= 0:
            self.remove(proxy)

    def reset(self, proxy: Proxy, score: str = setting.score_max):
        """
        重置代理的分数为初始分数
        :param proxy: 代理
        :param score: 初始分数
        :return:
        """
        if self.redis.hexists(self.all_proxy_key, proxy.string()):
            self.redis.hset(self.all_proxy_key, proxy.string(), score)
        else:
            raise KeyError(f"代理{proxy}不存在，无法重置")

    def increase(self, proxy: Proxy):
        """
        代理分数加一
        :param proxy: 代理
        :return:
        """
        self.redis.hincrby(self.all_proxy_key, proxy.string(), amount=1)

    def all_proxy(self):
        """
        获取全部代理的信息
        :return:
        """
        return [Proxy.str2proxy(s) for s in self.redis.hkeys(self.all_proxy_key)]

    def count_all_proxy(self):
        """
        统计全部的代理数量
        :return:
        """
        return len(self.all_proxy())

    def clear_valid_proxy(self):
        """
        清空有效代理数据
        :return:
        """
        self.redis.delete(self.valid_proxy_key)

    def add_valid_proxy(self, proxy: Proxy):
        """
        添加有效代理
        :param proxy:
        :return:
        """
        self.redis.sadd(self.valid_proxy_key, proxy.string())

    def count_valid_proxy(self):
        """
        统计有效代理数量
        :return:
        """
        return self.redis.scard(self.valid_proxy_key)

    def all_valid_proxy(self):
        """
        查看全部有效的代理
        :return:
        """
        return [Proxy.str2proxy(s) for s in self.redis.smembers(self.valid_proxy_key)]

    def a_valid_proxy(self):
        """
        返回一个有效的代理
        :return:
        """
        return Proxy.str2proxy(self.redis.srandmember(self.valid_proxy_key, 1)[0])


if __name__ == '__main__':
    rc = RedisClient()
    p = Proxy(ip="127.0.0.1", port=8080, protocol="http")
    rc.put(p)
    print(rc.get(p))
    rc.increase(p)
    print(rc.get(p))
    rc.reset(p)
    print(rc.get(p))
