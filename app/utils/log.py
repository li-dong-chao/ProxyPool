#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: log.py
@Time: 2023/2/2-22:32
@Author: Li Dongchao
@Desc: 
"""
import os

from app.config import setting

from loguru import logger

logger.add(os.path.join(setting.log_path, "{time:YYYY-MM-DD}.log"))
logger.add(os.path.join(setting.log_path, "error_{time:YYYY-MM-DD}.log"), level="ERROR")


if __name__ == '__main__':
    logger.info("日志测试")
