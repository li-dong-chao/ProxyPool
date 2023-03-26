#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: base.py
@Time: 2023/3/25-17:14
@Author: Li Dongchao
@Desc: 
"""

from abc import ABCMeta, abstractmethod
import warnings
from typing import Self, List, Generator
from urllib3.connectionpool import InsecureRequestWarning

from app.utils import logger, UACreator
from app.schemas.proxy import Proxy

# 过滤不安全的https连接警告
warnings.filterwarnings(action="ignore", category=InsecureRequestWarning)


class BaseFetcher(metaclass=ABCMeta):
    valid_subclasses: List[Self] = []
    logger = logger

    def __init__(self):
        self.uac = UACreator()

    @property
    def header(self):
        return {"user-agent": self.uac.get()}

    @abstractmethod
    def fetch(self) -> Proxy:
        """fetcher基类必须实现fetch方法，否则不会执行"""
        pass

    @classmethod
    def check(cls):
        """检测自定义fetcher是否满足基本结构"""
        valid_subclasses: List[Self] = []
        for subclass in cls.__subclasses__():
            try:
                tmp = subclass()  # 检查是否实现了fetch方法
                if isinstance(tmp.fetch(), Generator):  # 检查fetch方法是否为generator
                    valid_subclasses.append(subclass)  # noqa
                else:
                    cls.logger.warning(f"The fetch method of {subclass} is not generator.")
            except TypeError as _:
                cls.logger.warning(f"Can't find 'fetch' method in {subclass}")
        return valid_subclasses
