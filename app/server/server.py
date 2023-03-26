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
    return "ProxyPool"


@app.get("/get", summary="获取代理")
def get():
    try:
        proxy = manager.get_proxy()
        return proxy
    except EmptyPoolError as _:
        return "No proxy in pool."


@app.delete("/delete", summary="删除代理")
def delete(proxy: str):
    try:
        manager.delete_proxy(proxy)
        return "OK"
    except ValueError as _:
        return "Proxy format error."


@app.get("/quantity/all", summary="代理总数")
def quantity_all():
    return manager.quantity_all()


@app.get("/quantity/valid", summary="有效代理数")
def quantity_valid():
    return manager.quantity_valid()


def start_server():
    import uvicorn
    uvicorn.run("app.server.server:app", host="0.0.0.0", port=8000)


if __name__ == '__main__':
    start_server()
