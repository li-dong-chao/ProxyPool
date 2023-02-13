#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: ProxyPool.py
@Time: 2023/2/2-17:51
@Author: Li Dongchao
@Desc: 
@release: 
"""
import sys
import argparse
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from app.manager.manager import Manager
from app.server.server import start_server


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Proxy pool start tool."
            ""
            "You can use this tool start proxy pool server, fetcher and validator."
            "usage: "
            "   python3 ProxyPool.py start all        # Start server, fetcher and validator modules together."
            "   python3 ProxyPool.py start server     # Start server module."
            "   python3 ProxyPool.py start fetcher    # Start fetcher module."
            "   python3 ProxyPool.py start validator  # Start validator module."
            "You can also change \"start\" to \"stop\", this will stop the corresponding module."
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("action")
    parser.add_argument("module")
    args = parser.parse_args()
    action = args.action.lower()
    module = args.module.lower()
    if action not in ["start", "stop"]:
        raise ValueError("Parameter action should be \"start\" or \"stop\".")
    if module not in ["all", "server", "fetcher", "validator"]:
        raise ValueError("Parameter module should choose from \"all\", \"server\", \"fetcher\" and \"validator\"")
    if action == "start":
        manager = Manager()
        if module == "all":
            manager.add_fetch_scheduler()
            manager.add_validate_scheduler()
            start_server()
        elif module == "fetcher":
            manager.add_fetch_scheduler()
        elif module == "validator":
            manager.add_validate_scheduler()
        elif module == "server":
            start_server()


if __name__ == '__main__':
    main()
