#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: main.py
@Time: 2023/2/2-17:51
@Author: Li Dongchao
@Desc: 
@release: 
"""

import os
import sys
sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
from app import create_app

app = create_app()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
