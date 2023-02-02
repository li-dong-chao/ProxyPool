#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: run_server.py
@Time: 2023/2/2-17:51
@Author: Li Dongchao
@Desc: 
@release: 
"""

from fastapi import FastAPI

from app.api.api import router


app = FastAPI()

app.include_router(router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("run_server:app", host="127.0.0.1", port=8000)
