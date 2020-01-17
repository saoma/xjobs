# coding: utf-8
# Author：雪山凌狐
# website：http://www.xueshanlinghu.com
# version： 1.0
# update_date：2020-01-17

# 测试apscheduler与sqlite3数据库的结合
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

import time
from os.path import abspath, dirname
project_path = dirname(dirname(dirname(abspath(__file__))))
import sys
sys.path.append(project_path)
import xueshan_utils as xs_utils

def job1():
    '''
    用于测试的定时任务job1
    '''
    print("现在时间为：" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))


if __name__ == '__main__':
    # 测试代码
    EXECUTORS = {
        'default': ThreadPoolExecutor(max_workers=30),
        'processpool': ProcessPoolExecutor(max_workers=30)
    }
    job_defaults = {
        'coalesce': True,  # 积攒的任务只跑一次
        'max_instances': 1,  # 只能有一个实例并发
        'misfire_grace_time': 60  # 60秒的任务超时容错
    }
    # jobstores = {
    #     # 定义下述sqlite代码，会将任务保存到当前目录的xjobs_testsqlite.db数据库中，因为指定了表名
    #     # 所以会自动创建表名，三列，id（应该是md5值），next_run_time（下次运行的时间戳，用一个点包含毫秒应该）
    #     # 还有一列是job_state（猜应该是任务状态，BLOB大字段，存储的是HEX值，看不懂）
    #     'default': SQLAlchemyJobStore(url='sqlite:///xjobs_testsqlite.db', tablename='xjobs_test1')
    # }
    jobstores = {
        # 定义下述sqlite代码，表名是已存在的现成表，但没有其他参数，会直接报错，说表内没有id字段，所以不能这么定义
        'default': SQLAlchemyJobStore(url='sqlite:///xjobs_testsqlite.db', tablename='xjobs_task')
    }
    scheduler = BackgroundScheduler(jobstores=jobstores, executors=EXECUTORS, job_defaults=job_defaults)
    cron_expression = xs_utils.to_cron("*/3 * * * * *")
    scheduler.add_job(job1, 'cron', jitter=1, start_date='2020-01-15', end_date='2020-12-17', **cron_expression)
    try:
        scheduler.start()
        # BackgroundScheduler这个调度器，开始后不会阻塞，可以继续执行后续的代码。如果后续没有其他代码了，可以使用死循环等待下一步操作
        while True:
            time.sleep(0.5)
    except Exception as e:
        scheduler.shutdown(False)
        print(e)


# 结论：
# 当不定义jobstores的情况下，默认的jobstores为内存存储，存储的依然还是id、next_run_time、job_state等字段
# 因此我们的调度框架，如果是不打算做持久化存储到数据库这些信息的话，使用内存作为jobstores即可
# 如果需要启动定时调度框架，则启动框架的python主控程序，如果要停止定时调度框架，则关闭python主控程序即可，很方便。
# 后续将按该思路进行后续设计