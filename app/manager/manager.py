#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: manager.py
@Time: 2023/2/3-17:15
@Author: Li Dongchao
@Desc: 
@release: 
"""
import datetime
from queue import Queue
from threading import Thread
from apscheduler.schedulers.blocking import BlockingScheduler

from app.fetcher.fetcher import Fetcher
from app.schemas.proxy import Proxy
from app.validator.validator import Validator
from app.db.redis_client import RedisClient
from app.utils import logger
from app.config import setting
from app.exception import AllValidError


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
        for cur_proxy in self.fetcher.get():
            # 如果超过预期代理数量上限，删除分数最低的
            # 如果全部都是有效的了，就放弃本次新代理的入库
            if self.db.all() >= setting.max_proxy_limit:
                try:
                    last = self.db.last()
                    self.db.remove(last)
                    self.db.add(proxy=cur_proxy)
                except AllValidError as _:
                    self.save()
                    return
        self.save()

    def validate(self, proxy: Proxy):
        """
        验证代理的有效性
        """
        self.logger.info(f"开始验证{proxy}")
        is_valid = Validator.check_proxy(proxy)
        if is_valid:
            self.db.max(proxy)
        else:
            self.db.decrease(proxy)

    def validate_all(self):
        """多线程验证数据库中的代理"""
        all_proxies = self.db.all()
        self.logger.info(f"当前数据库中有{self.db.count()}条数据，即将开始验证代理有效性...")
        q = Queue()  # 使用Queue实现多线程间的数据共享
        [q.put(proxy) for proxy in all_proxies]
        while not q.empty():
            thread_list = []
            for i in range(setting.validate_thread_nums):
                proxy = q.get()
                t = Thread(target=self.validate, args=(proxy, ))
                thread_list.append(t)
            for t in thread_list:
                t.start()
            for t in thread_list:
                t.join()
        self.db.save()
        self.logger.info(f"已验证{self.db.count()}条代理数据，"
                         f"其中有效代理{self.db.count_max()}条")

    def get_proxy(self):
        """
        返回一个有效代理
        :return:
        """
        return self.db.get().string()

    def delete_proxy(self, proxy_str: str):
        """删除代理"""
        proxy = Proxy.str2proxy(proxy_str)
        self.db.remove(proxy)

    def quantity_all(self):
        """查询代理总数"""
        return self.db.count()

    def quantity_valid(self):
        """查询有效代理总数"""
        return self.db.count_max()

    def save(self):
        """数据持久化"""
        self.db.save()

    def add_fetch_scheduler(self):
        """创建抓取代理ip定时任务"""
        scheduler = BlockingScheduler()
        scheduler.add_job(
            self.fetch,
            trigger='interval',
            hours=setting.fetch_interval,
            next_run_time=datetime.datetime.now()
        )
        scheduler.start()

    def add_validate_scheduler(self):
        """创建验证代理ip定时任务"""
        scheduler = BlockingScheduler()
        scheduler.add_job(
            self.validate_all,
            trigger='interval',
            hours=setting.validate_interval,
            next_run_time=datetime.datetime.now()

        )
        scheduler.start()


if __name__ == '__main__':
    manager = Manager()
    manager.fetch()
    manager.validate_all()
    print(manager.db.all())
