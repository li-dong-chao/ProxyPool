#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: config.py
@Time: 2023/2/2-22:36
@Author: Li Dongchao
@Desc: 
"""

import os


class Setting(object):

    root_path: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_path: str = os.path.join(root_path, "log")

    def __init__(self):
        os.makedirs(self.log_path, exist_ok=True)


setting = Setting()
