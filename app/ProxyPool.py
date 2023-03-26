#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File: ProxyPool.py
@Time: 2023/2/2-17:51
@Author: Li Dongchao
@Desc: 
@release: 
"""
import os
import sys
import signal
import argparse
from os.path import dirname, abspath
from multiprocessing import Process
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from app.manager.manager import Manager
from app.server.server import start_server
from app.config import setting


def start_server_in_son_process():
    """server启动方法"""
    with open(setting.server_pid_path, 'w', encoding="utf-8") as f:
        f.write(str(os.getpid()))
    start_server()


def start_fetcher_in_son_process():
    """fetcher启动方法"""
    with open(setting.fetcher_pid_path, 'w', encoding="utf-8") as f:
        f.write(str(os.getpid()))
    manager = Manager()
    manager.add_fetch_scheduler()


def start_validator_in_son_process():
    """validator启动方法"""
    with open(setting.validator_pid_path, 'w', encoding="utf-8") as f:
        f.write(str(os.getpid()))
    manager = Manager()
    manager.add_validate_scheduler()


def kill(module: str):
    """关闭进程"""
    pid_path = getattr(setting, f"{module}_pid_path")
    with open(pid_path, "r", encoding="utf-8") as f:
        pid = int(f.read().strip())
    if sys.platform == "win32":
        os.popen(f"taskkill.exe /F /pid:{pid}")
        os.remove(pid_path)
    elif sys.platform == "linux":
        os.kill(pid, signal.SIGKILL)
        os.remove(pid_path)
    else:
        raise ValueError("Unsupported system.")


def main():
    # todo: 暂时还未实现守护进程启动
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
        raise ValueError("Parameter action should be start or stop.")
    if module not in ["all", "server", "fetcher", "validator"]:
        raise ValueError("Parameter module should choose from \"all\", \"server\", \"fetcher\" and \"validator\"")
    if action == "start":
        if module == "all":
            p1 = Process(target=start_fetcher_in_son_process)
            p2 = Process(target=start_validator_in_son_process)
            p3 = Process(target=start_server_in_son_process)
            p1.start()
            p2.start()
            p3.start()
        elif module == "fetcher":
            p = Process(target=start_fetcher_in_son_process)
            p.start()
        elif module == "validator":
            p = Process(target=start_validator_in_son_process)
            p.start()
        elif module == "server":
            p = Process(target=start_server_in_son_process)
            p.start()
    elif action == "stop":
        if module == "all":
            kill("server")
            kill("validator")
            kill("fetcher")
        else:
            kill(module)


if __name__ == '__main__':
    main()
