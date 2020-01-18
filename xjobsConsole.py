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


def get_format_time(format='%Y-%m-%d %H:%M:%S'):
    '''
    获取现行时间格式化后的时间文本
    :param format: 传入format，默认为%Y-%m-%d %H:%M:%S
    【常用format代码指引】
    %Y  Year with century as a decimal number.
    %m  Month as a decimal number [01,12].
    %d  Day of the month as a decimal number [01,31].
    %H  Hour (24-hour clock) as a decimal number [00,23].
    %M  Minute as a decimal number [00,59].
    %S  Second as a decimal number [00,61].
    %z  Time zone offset from UTC.
    %a  Locale's abbreviated weekday name.
    %A  Locale's full weekday name.
    %b  Locale's abbreviated month name.
    %B  Locale's full month name.
    %c  Locale's appropriate date and time representation.
    %I  Hour (12-hour clock) as a decimal number [01,12].
    %p  Locale's equivalent of either AM or PM.
    :return: 返回现行时间格式化后的文本字符串
    '''
    return time.strftime(format, time.localtime())

def my_help():
    '''
    显示中控台帮助信息
    '''
    print("【帮助文档】中控台支持如下几种命令输入方式:")
    print("1、帮助-[help]")
    print("2、导出当前任务情况-[exportTask]")
    print("3、暂停某一具体job-[pause_job job_id]")
    print("4、查看具体job情况-[query_job job_id]")
    print("5、重新加载所有任务-[reloadTask]")
    print("6、更新加载所有任务-[updateTask]")
    print("9、退出程序-[quit]")
    print("功能1、2、5、6、9可以直接输入数字处理，否则请直接输入方括号中的命令")
    print("")

def my_exportTask():
    pass

def my_pausejob(s_cmd):
    pass

def my_getjob(s_cmd):
    pass

def load_task(flag):
    pass

def my_exit():
    pass

if __name__ == '__main__':
    # 中控台启动后的运行代码

    # 将当前运行的cmd程序标题重命名
    os.system("title xjobs定时调度程序")
    print("现在的时间是%s" % get_format_time())
    print("xjobs定时调度程序已启动，正在初始化...")

    # 日志设置
    log_time = get_format_time(format='%Y%m%d%H%M%S')
    # print(log_time)
    log_foldername = "xjobs_log"
    if not(os.path.exists(log_foldername)):
        os.mkdir(log_foldername)
    log_filename = log_foldername + '\\log_' + log_time + '.log'
    logging.basicConfig(level=logging.DEBUG,
                        # level=logging.INFO,
                        # format='[%(asctime)s] %(pathname)s[line:%(lineno)d] %(levelname)s: %(message)s',
                        format='[%(asctime)s] %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=log_filename,
                        filemode='w')
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    logging.info("现在的时间是%s" % get_format_time())
    logging.info("xjobs定时调度程序已启动，正在初始化...")

    # scheduler配置设置
    executors = {
        'default': ThreadPoolExecutor(max_workers=30),
        'processpool': ProcessPoolExecutor(max_workers=30)
    }
    job_defaults = {
        'coalesce': True,  # 积攒的任务只跑一次
        'max_instances': 1,  # 只能有一个实例并发
        'misfire_grace_time': 60  # 60秒的任务超时容错
    }
    scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults)

    # 定时任务启动
    try:
        scheduler.start()
    except Exception as e:
        scheduler.shutdown(False)
        s = traceback.format_exc()
        print("调度器启动报错，错误信息为：\n" + s)
        logging.error("调度器启动报错，错误信息为：\n" + s)

    print("定时调度程序初始化完毕！\n" + '-' * 40)
    logging.info("定时调度程序初始化完毕！")
    # 先展示一次帮助信息
    my_help()
    # 进行循环其他指令
    while True:
        try:
            print("请输入需要操作的命令，输入help查看帮助信息：")
            s_cmd = input(">>>")
            print("输入的命令为：%s\n执行中..." % s_cmd)
            if s_cmd == "help" or s_cmd == "1":
                my_help()
            elif s_cmd == "exportTask" or s_cmd == "2":
                my_exportTask()
            elif s_cmd.find('pause_job ') > -1:
                my_pausejob(s_cmd)
            elif s_cmd.find('query_job ') > -1:
                my_getjob(s_cmd)
            elif s_cmd == "reloadTask" or s_cmd == "5":
                load_task(1)
            elif s_cmd == "updateTask" or s_cmd == "6":
                load_task(0)
            elif s_cmd == "quit" or s_cmd == "9":
                my_exit()
            else:
                print("无法处理该命令，请重新输入！")
        except Exception as e:
            print("中控台执行报错，错误信息为：\n" + s)
            logging.error("中控台执行报错，错误信息为：\n" + s)