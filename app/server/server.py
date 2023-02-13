#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: server.py
@Time: 2023/2/2-17:11
@Author: Li Dongchao
@Desc: 
@release: 
"""

from fastapi import FastAPI

from app.manager.manager import Manager
from app.exception import EmptyPoolError

app = FastAPI()

manager = Manager()


@app.get("/")
def index():
    return "ProxyPoll"


@app.get("/get", summary="获取代理")
def get():
    try:
        proxy = manager.get_proxy()
        return proxy
    except EmptyPoolError as _:
        return "No proxy in pool now, please check whether the fetcher is work"


def start_server():
    import uvicorn
    uvicorn.run("app.server.server:app", host="127.0.0.1", port=8000)


if __name__ == '__main__':
    start_server()
