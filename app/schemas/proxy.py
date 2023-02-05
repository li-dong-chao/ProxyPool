#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: proxy.py
@Time: 2023/2/2-16:40
@Author: Li Dongchao
@Desc: 定义代理类，包含对代理验证等。
@release: 
"""

import re
from enum import Enum
from pydantic import BaseModel, Field


class Protocol(Enum):
    http: str = "http"
    https: str = "https"

    def __str__(self):
        return self.value


class Proxy(BaseModel):
    ip: str = Field(regex=r"((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}")
    port: int = Field(ge=1, le=65535)
    protocol: Protocol

    @staticmethod
    def str2proxy(s: str):
        """
        字符串转代理
        :param s:
        :return:
        """
        regex = re.compile(r"^(http|https)://"
                           r"((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}:"
                           r"\d{1,5}$")
        if re.match(regex, s):
            protocol, last = s.split("://")
            ip, port = last.split(":")
            return Proxy(ip=ip, port=port, protocol=protocol)
        else:
            raise ValueError(f"字符串格式 [{s}] 错误，无法转化为代理")

    def __str__(self):
        return f"{self.protocol}://{self.ip}:{self.port}"

    def string(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.__str__())


if __name__ == '__main__':
    # p1 = Proxy(ip="124.220.168.140", port=3128, protocol="http1")
    # print(f"Proxy is {p1}")
    print(Proxy.str2proxy("https://127.0.0.1:8000"))
