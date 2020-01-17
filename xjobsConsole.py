# coding: utf-8
# Author：雪山凌狐
# website：http://www.xueshanlinghu.com
# version： 1.0
# update_date：2020-01-17

# xjobs中控台程序（主程序） 双击打开即启动xjobs

from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR,EVENT_JOB_MISSED,EVENT_JOB_MAX_INSTANCES
import logging
import time
import subprocess
import traceback
import os


if __name__ == '__main__':
    # 中控台启动后的运行代码

    # 将当前运行的cmd程序标题重命名
    os.system("title xjobs定时调度程序")
    input()