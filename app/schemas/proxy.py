#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: proxy.py
@Time: 2023/2/2-16:40
@Author: Li Dongchao
@Desc: 定义代理类，包含对代理验证等。
@release: 
"""

from pydantic import BaseModel, Field


class Proxy(BaseModel):
    ip: str = Field(regex=r"((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}")
    port: int = Field(ge=1, le=65535)

    def __str__(self):
        return f"{self.ip}:{self.port}"

    def string(self):
        return self.__str__()


if __name__ == '__main__':
    p1 = Proxy(ip="127.0.0.1", port="123")
    print(f"String is {p1}")
