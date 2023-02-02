#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: useragent_creator.py
@Time: 2023/2/2-21:39
@Author: Li Dongchao
@Desc: 参考fake-useragent项目实现一个简单的ua生成器
"""

import os
import json
import random


class UACreator(object):

    def __init__(self):
        self.db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "browsers.json")
        self.db = {}
        self._load()

    def _load(self):
        with open(self.db_file, "r", encoding="utf-8") as f:
            for line in f.readlines():
                self.db.update(json.loads(line))

    def _get_ua(self, browser: str):
        return random.choice(self.db.get(browser))

    @property
    def chrome(self):
        return self._get_ua("chrome")

    @property
    def opera(self):
        return self._get_ua("opera")

    @property
    def firefox(self):
        return self._get_ua("firefox")

    @property
    def safari(self):
        return self._get_ua("safari")

    @property
    def edge(self):
        return self._get_ua("edge")

    @property
    def ie(self):
        return self._get_ua("internet explorer")

    def get(self):
        browser = random.choice(['chrome', 'opera', 'firefox', 'safari', 'edge', 'internet explorer'])
        return self._get_ua(browser)


if __name__ == '__main__':
    uac = UACreator()
    print(uac.ie)
