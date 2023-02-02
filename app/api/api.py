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

from app.api.endpoints import test

router = APIRouter()

router.include_router(test.router)
