#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: pool.py
@Time: 2023/2/3-13:58
@Author: Li Dongchao
@Desc: 连接池
@release: 
"""

from redis import BlockingConnectionPool

from app.config import setting

redis_pool = BlockingConnectionPool(
    host=setting.redis_config.host,
    port=setting.redis_config.port,
    username=setting.redis_config.username,
    password=setting.redis_config.password,
    max_connections=setting.redis_config.max_connections,
    timeout=setting.redis_config.timeout,
    decode_responses=True
)

