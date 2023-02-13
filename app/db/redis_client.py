#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: redis_client.py
@Time: 2023/2/3-13:48
@Author: Li Dongchao
@Desc: redis客户端
@release: 
"""
from typing import List
from random import choice
from redis import StrictRedis

from app.utils import logger
from app.config import setting
from app.db.pool import redis_pool
from app.schemas.proxy import Proxy
from app.exception import EmptyPoolError


class RedisClient(object):
    """
    redis数据库

    包含了代理池用到的相关的数据库操作
    """

    def __init__(self):
        self.proxy_key = setting.key_name
        self._redis = StrictRedis(connection_pool=redis_pool)

    def add(self, proxy: Proxy) -> None:
        """
        新增一个代理，并给其分数初始化
        :param proxy: 代理
        :return:
        """
        if not self.exists(proxy):
            self._redis.zadd(self.proxy_key, {proxy.string(): setting.score_init})

    def get_score(self, proxy: Proxy) -> float:
        """
        获取指定代理的分数信息
        :param proxy: 代理
        :return:
        """
        return int(self._redis.zscore(self.proxy_key, proxy.string()))

    def exists(self, proxy: Proxy):
        return not self._redis.zscore(self.proxy_key, proxy.string()) is None

    def remove(self, proxy: Proxy) -> None:
        """
        从数据库中删除代理
        :param proxy: 代理
        :return:
        """
        self._redis.zrem(self.proxy_key, proxy.string())

    def decrease(self, proxy: Proxy) -> None:
        """
        代理分数减一
        :param proxy: 代理
        :return:
        """
        self._redis.zincrby(self.proxy_key, amount=-1, value=proxy.string())
        score = self.get_score(proxy)
        logger.info(f"{proxy} score decrease 1, current {score}.")
        if score <= setting.score_min:
            logger.info(f'{proxy} current score {score}, remove')
            self.remove(proxy)

    def max(self, proxy: Proxy) -> None:
        """
        重置代理的分数为最大分数
        :param proxy: 代理
        :return:
        """
        if self.exists(proxy):
            self._redis.zadd(self.proxy_key, {proxy.string(): setting.score_max})
            logger.info(f"max {proxy} score to {setting.score_max}")
        else:
            raise ValueError(f"Can't find {proxy}，max error")

    def all(self) -> List[Proxy]:
        """
        获取全部代理的信息
        :return:
        """
        return [Proxy.str2proxy(x)
                for x in self._redis.zrangebyscore(self.proxy_key,
                                                   min=setting.score_min,
                                                   max=setting.score_max)]

    def count(self) -> int:
        """
        统计全部的代理数量
        :return:
        """
        return self._redis.zcount(self.proxy_key, min=setting.score_min, max=setting.score_max)

    def count_max(self) -> int:
        """统计有效代理的数量"""
        return self._redis.zcount(self.proxy_key, min=setting.score_max, max=setting.score_max)

    def get(self) -> Proxy:
        """
        从数据库中获取一个代理

        优先从有效代理中获取，如果不存在的话再去根据分数的从高到低顺序获取代理，
        如果没有代理，报代理为空异常。
        :return:
        """
        valid_proxies: list = self._redis.zrangebyscore(self.proxy_key, min=setting.score_max, max=setting.score_max)
        if valid_proxies:
            return Proxy.str2proxy(choice(valid_proxies))
        proxies: list = self._redis.zrangebyscore(self.proxy_key, min=setting.score_min, max=setting.score_max)
        if proxies:
            return Proxy.str2proxy(proxies[0])
        else:
            raise EmptyPoolError("No proxy in pool.")

    def save(self):
        """对redis中的数据进行持久化存储"""
        self._redis.save()


if __name__ == '__main__':
    rc = RedisClient()
    p = Proxy(ip="127.0.0.1", port=8080, protocol="http")
    rc.add(p)
    rc.max(p)
    rc.decrease(p)
    print(rc.count())
    print(rc.count_max())
