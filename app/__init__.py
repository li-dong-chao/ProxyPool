#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: __init__.py.py
@Time: 2023/2/2-15:02
@Author: Li Dongchao
@Desc: 
@release:
"""

from fastapi import FastAPI

from app.api.api import router, manager


def create_app():
    app = FastAPI()

    app.include_router(router)

    # @app.on_event("startup")
    def start():
        manager.fetch()
        manager.validate_all()

    return app
