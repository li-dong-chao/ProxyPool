#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: config.py
@Time: 2023/2/2-22:36
@Author: Li Dongchao
@Desc: 
"""

import os


class RedisConfig(object):
    host: str = "127.0.0.1"
    port: int = 6379
    username: str = ""
    password: str = ""
    db: int = 0
    max_connections: int = 10
    timeout: int = 10
    socket_connect_timeout: int = 10


class Setting(object):

    # 目录配置
    root_path: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_path: str = os.path.join(root_path, "log")

    # redis配置
    redis_config = RedisConfig()
    key_name: str = "proxy"

    # 代理分数配置
    score_init: int = 10
    score_max: int = 100
    score_min: int = 0

    # 定时任务配置，单位: 小时
    fetch_interval: int = 6
    validate_interval: int = 3

    # 多线程配置
    fetch_thread_nums: int = 10
    validate_thread_nums: int = 10

    def __init__(self):
        os.makedirs(self.log_path, exist_ok=True)


setting = Setting()
