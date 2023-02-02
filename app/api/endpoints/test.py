#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: test.py
@Time: 2023/2/2-17:12
@Author: Li Dongchao
@Desc: 测试代理ip活性使用的接口
@release: 
"""

from fastapi import APIRouter, Request


router = APIRouter()


@router.get("/test")
def test(request: Request):
    return {"host": request.client.host, "port": request.client.port}
