# coding: utf-8
# Author：雪山凌狐
# website：http://www.xueshanlinghu.com
# version： 1.0
# update_date：2020-01-19

# 测试后台模式运行的定时任务运行
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

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

def job2(number, **kwargs):
    '''
    用于测试的定时任务job2
    '''
    print("我是job2")
    print(number + 1)
    print(kwargs.get("name"))

if __name__ == '__main__':
    # 测试代码
    EXECUTORS = {
        'default': ThreadPoolExecutor(max_workers=30),
        'processpool': ProcessPoolExecutor(max_workers=30)
    }
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': True,  # 积攒的任务只跑一次
        'max_instances': 1,  # 只能有一个实例并发
        'misfire_grace_time': 60  # 60秒的任务超时容错
    }
    scheduler = BackgroundScheduler(executors=EXECUTORS, job_defaults=SCHEDULER_JOB_DEFAULTS)
    # 获取时间表达式dict，测试的表达式的含义为每3秒执行一次
    '''
    【cron表达式介绍】
    *：触发所有值
    */a：a从最小值开始，触发每个值
    a-b：触发a-b范围内的任何值（必须小于b）
    a-b/c：触发在a-b之间的每个c值
    xth y：第y个工作日中第x天发触发
    last x：在一个月中第x个工作日中的最后一天触发
    last：在月末的最后一天触发
    x,y,z：触发任何匹配的表达式; 可以组合任意数量的任何上述表达式。
    注意：xth y,last x,last这3个是用在day（即日）参数中，其它所有参数都可以使用。
    '''
    cron_expression = xs_utils.to_cron("*/3 * * * * *")
    # 添加job任务到调度器
    # jitter表示随机扰动，给每次触发添加一个随机浮动秒数，一般适用于多服务器，避免同时运行造成服务拥堵。可省略
    # start_date表示开始日期，日期大于等于该日就能运行。可省略，也可传入None表示省略
    # end_date表示结束日期，日期小于该日才能运行，等于不运行。可省略，也可传入None表示省略
    # **cron_expression的写法，可以以dict方式传入时间表达式，也可传入None表示省略
    scheduler.add_job(job1, 'cron', jitter=1, start_date='2020-01-15', end_date='2020-12-17', **cron_expression)
    # job2加入
    scheduler.add_job(job2, 'cron', id="id_job2", args=(1,), kwargs={'name': "job2_name"}, **cron_expression)
    try:
        scheduler.start()

        # 测试获取jobs状态
        jobs = scheduler.get_jobs()
        for job in jobs:
            print("当前job信息：", "job.id：%s" % job.id, "job.name：%s" % job.name)
        # 通过get_job命令获取某个特别id的job信息，成功返回Job，失败返回None
        my_job2 = scheduler.get_job('id_job2')
        if my_job2:
            job = my_job2
            print(job)
            print("当前job信息：", "job.id：%s" % job.id, "job.name：%s" % job.name)
            print("已找到相关job[job_id = %s]的信息：" % job.id)
            print('id：', job.id)
            print('name[任务名]：', job.name)
            print('trigger[触发器]：', job.trigger)
            print('next_run_time[下一次运行时间]：', job.next_run_time)
            print('coalesce[积攒的任务是否只跑一次]：', job.coalesce)
            print('max_instances[实例最大并发数]：', job.max_instances)
            print('misfire_grace_time[任务超时多少秒后不再重跑]：', job.misfire_grace_time)
            print('executor[执行器名]：', job.executor)
            print('func_ref[函数调用信息]：', job.func_ref)
            print('kwargs[job执行传入的字典]：', job.kwargs)
            print('args[job执行传入的参数]：', job.args)
            print('-' * 40)

        # BackgroundScheduler这个调度器，开始后不会阻塞，可以继续执行后续的代码。如果后续没有其他代码了，可以使用死循环等待下一步操作
        while True:
            time.sleep(0.5)
    except Exception as e:
        scheduler.shutdown(False)
        print(e)

