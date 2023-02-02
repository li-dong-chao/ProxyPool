#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: vaildator.py
@Time: 2023/2/2-16:01
@Author: Li Dongchao
@Desc: 代理ip检查器，检查代理ip格式是否正确以及其活性
@release: 
"""

import re


class Validator(object):

    # 验证代理活性使用的header
    header = {
        "user-agent": ("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36")
    }

    def __init__(self, proxy):
        self.proxy = proxy

    def http_ok(self):
        pass

    def https_ok(self):
        pass



if __name__ == '__main__':
    v = Validator("1.1.1.1:888")
    print(v.is_proxy)
