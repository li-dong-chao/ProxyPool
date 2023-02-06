#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: api.py
@Time: 2023/2/2-17:11
@Author: Li Dongchao
@Desc: 
@release: 
"""

from fastapi import APIRouter

from app.manager.manager import Manager

router = APIRouter()

manager = Manager()


@router.get("/get", summary="获取一个代理")
def get():
    return manager.get_proxy()
