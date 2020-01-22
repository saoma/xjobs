# coding: utf-8
# Author：雪山凌狐
# website：http://www.xueshanlinghu.com
# version： 1.0
# update_date：2020-01-22

# xjobs中控台程序（主程序） 双击打开即启动xjobs

from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR,EVENT_JOB_MISSED,EVENT_JOB_MAX_INSTANCES
import logging
import time
import subprocess
import traceback
import os
import xueshan_utils as xs_utils


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
    print("3、暂停具体job(s)，支持多个输入，每个id之间使用英文,分隔即可-[pause_job job_id(s)]")
    print("4、恢复具体job(s)，支持多个输入，每个id之间使用英文,分隔即可-[resume_job job_id(s)]")
    print("5、查看具体job(s)情况，支持多个输入，每个id之间使用英文,分隔即可-[get_job job_id(s)]")
    print("6、重新加载所有任务-[reloadTask]")
    print("7、更新加载所有任务-[updateTask]")
    print("8、查看所有job(s)的情况，详细情况flag传入1，简略情况flag传入0-[get_all_jobs flag]")
    print("9、退出程序-[quit]")
    print("功能1、2、6、7、9可以直接输入数字处理，否则请直接输入方括号中的命令")
    print("")

def my_exportTask():
    '''
    导出目前的任务列表
    '''
    # 获取到所有调度器的job信息
    scheduler.resume_job()
    jobs = scheduler.get_jobs()
    if jobs:
        now_time = get_format_time()
        export_time = now_time.replace("-", "").replace(":", "").replace(" ", "")
        export_foldername = "xjobs_exportTask"
        if not (os.path.exists(export_foldername)):
            os.mkdir(export_foldername)
        export_filename = export_foldername + '\\exportTask_' + export_time + '.txt'
        # 写入导出的文件中
        with open(export_filename, 'w', encoding='utf-8') as f:
            print("%s 当前时间定时任务情况如下:" % now_time)
            f.write("%s 当前时间定时任务情况如下:" % now_time)
            for job in jobs:
                f.write("\n")
                print("job_id=%s" % job.id, "job_name=%s" % job.name, job)
                f.write("job_id=%s" % job.id + " " + "job_name=%s" % job.name + " " + job)
        print("执行成功，具体数据请查看文件[%s]" % export_filename)
    else:
        print("目前调度程序中暂时没有job")

def my_pausejobs(s_cmd):
    '''
    暂停具体的job(s)，支持多个输入，以,分隔处理
    :param s_cmd:以pause_job 开头的命令，后面跟随具体的job_id，会暂停它们
    '''
    job_id = s_cmd.replace("pause_job", "").strip()
    job_ids = job_id.split(",")
    for per_job_id in job_ids:
        if scheduler.get_job(per_job_id) is not None:
            scheduler.pause_job(per_job_id)
            print("已找到并暂停相关job[job_id = %s]" % per_job_id)
            logging.info("已找到并暂停相关job[job_id = %s]" % per_job_id)
        else:
            print("未找到对应的job[job_id = %s]去暂停" % per_job_id)
            logging.info("未找到对应的job[job_id = %s]去暂停" % per_job_id)
    print("暂停具体的job(s)完成！")

def my_resumejobs(s_cmd):
    '''
    恢复具体的job(s)，支持多个输入，以,分隔处理
    :param s_cmd:以resume_job 开头的命令，后面跟随具体的job_id，会恢复它们
    '''
    job_id = s_cmd.replace("resume_job", "").strip()
    job_ids = job_id.split(",")
    for per_job_id in job_ids:
        if scheduler.get_job(per_job_id) is not None:
            scheduler.resume_job(per_job_id)
            print("已找到并恢复相关job[job_id = %s]" % per_job_id)
            logging.info("已找到并恢复相关job[job_id = %s]" % per_job_id)
        else:
            print("未找到对应的job[job_id = %s]去恢复" % per_job_id)
            logging.info("未找到对应的job[job_id = %s]去恢复" % per_job_id)
    print("恢复具体的job(s)完成！")

def my_getjobs(s_cmd):
    '''
    获取具体的job(s)，支持多个输入，以,分隔处理
    :param s_cmd:以get_job 开头的命令，后面跟随具体的job_id，会分别获取它们的状态
    '''
    job_id = s_cmd.replace("get_job", "").strip()
    job_ids = job_id.split(",")
    for per_job_id in job_ids:
        if scheduler.get_job(per_job_id) is not None:
            job = scheduler.get_job(per_job_id)
            logging.info("已找到相关job[job_id = %s]的信息" % per_job_id)
            print("已找到相关job[job_id = %s]的信息：" % per_job_id)
            if job.next_run_time is None:
                logging.info("【该job在调度器中已被暂停】")
                print("【该job在调度器中已被暂停】")
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
        else:
            print("未找到对应的job[job_id = %s]" % per_job_id)
            print('-' * 40)
            logging.info("未找到对应的job[job_id = %s]" % per_job_id)
    print("获取具体的job(s)信息完成！")

def sqlite3_query(sql, param=None):
    '''
    调用现有的sqlite3封装库进行查询
    :param sql: sql查询语句
    :param param: 查询传入的参数，默认为空
    :return: 查询后返回的fetchall结果，一个list
    '''
    sqlite = xs_utils.xsSqlite3(database_path)
    res = sqlite.query(sql, param)
    sqlite.close_all()
    return res

def load_task(flag):
    '''
    加载任务，全部加载或者更新加载
    :param flag: 当flag为1的时候为reloadTask重新加载所有的任务，当flag为0的时候为updateTask只重新加载15分钟前更新的任务
    '''
    jobs = scheduler.get_jobs()
    joblist = []
    for job in jobs:
        joblist.append(job.id)

    # 从数据库中获取所有jobs配置列表
    if flag == 1 :
        sql = '''select a.job_id, a.job_name, a.command_lang, a.command, a.input_param, a.cron_exp,
                    a.start_date, a.end_date, a.jitter, coalesce(a.is_pause, 0) is_pause, a.success_exit, a.update_time
                from xjobs_task a'''
    else :
        sql = '''select a.job_id, a.job_name, a.command_lang, a.command, a.input_param, a.cron_exp,
                    a.start_date, a.end_date, a.jitter, coalesce(a.is_pause, 0) is_pause, a.success_exit, a.update_time
                from xjobs_task a
                where a.update_time >= datetime('now', 'localtime', '-15 minute')'''
    res = sqlite3_query(sql)
    # 每个查到的结果遍历
    if res:
        for row in res:
            # 组装返回结果字典
            row_dict = {}
            row_dict["job_id"] = str(row[0])
            row_dict["job_name"] = row[1]
            row_dict["command_lang"] = row[2]
            row_dict["command"] = row[3]
            row_dict["input_param"] = row[4]
            row_dict["cron_exp"] = row[5]
            row_dict["start_date"] = row[6]
            row_dict["end_date"] = row[7]
            row_dict["jitter"] = row[8]
            row_dict["is_pause"] = row[9]
            row_dict["success_exit"] = row[10]
            row_dict["update_time"] = row[11]
            print(row_dict)
            cron_expression = xs_utils.to_cron(row_dict.get('cron_exp'))
            executor = 'processpool'
            # 如果一开始读取时该任务被定义为暂停任务且还未加入调度器，则直接跳过，不创建
            if row_dict["job_id"] not in joblist and row_dict["is_pause"] == 1:
                pass
            # 表中已暂停启用的任务，如果还在调度器中，则删除该任务
            elif row_dict["job_id"] in joblist and row_dict["is_pause"] == 1:
                print("存储器中该job_id已停用，调度器中删除该job[job_id = %s]" % row_dict["job_id"])
                scheduler.remove_job(row_dict["job_id"])
            # 否则创建任务
            else:
                scheduler.add_job(func=job_run,
                    args=(row_dict['job_id'], row_dict['job_name'], row_dict['command_lang'], row_dict['command'],
                          row_dict['input_param'], row_dict['success_exit']),
                    id=row_dict['job_id'],
                    name=row_dict['job_name'],
                    replace_existing=True,   # 若已存在该任务，则覆盖
                    trigger='cron',
                    executor=executor,
                    start_date=row_dict["start_date"],
                    end_date=row_dict["end_date"],
                    jitter=row_dict["jitter"],
                    **cron_expression)
    else:
        print("没有需要加载的任务！")
        logging.info("没有需要加载的任务！")
    if flag == 1:
        print("重新加载所有任务执行完毕！")
        logging.info("重新加载所有任务执行完毕！")
    else:
        print("更新加载所有任务执行完毕！")
        logging.info("更新加载所有任务执行完毕！")

def job_run(job_id, job_name, command_lang, command, input_param, success_exit):
    '''
    job调度的模板程序代码
    :param job_id:任务id
    :param job_name:任务名称
    :param command_lang:命令语言类型
    :param command:命令
    :param input_param:命令参数
    :param success_exit:成功执行任务所会输出的文本
    '''
    # 记录任务开始执行
    logging.info("开始执行job：[job_id=%s，job_name=%s]" % (job_id, job_name))
    print("开始执行job：[job_id=%s，job_name=%s]" % (job_id, job_name))
    # 初始化返回代码以及返回信息
    return_code = -1
    return_str = ''

    try:
        if command_lang == 'python':
            return_code, return_str = job_python(command, input_param, success_exit)
        elif command_lang == 'cmd':
            return_code, return_str = job_cmd(command, success_exit)
        else:
            logging.error("当前指定的任务类型comman_lang[%s]定时调度程序不支持，已跳过不执行！" % command_lang)
            print("当前指定的任务类型comman_lang[%s]定时调度程序不支持，已跳过不执行！" % command_lang)
    except Exception as e:
        s = traceback.format_exc()
        logging.error("执行定时任务失败[job_id=%s，job_name=%s]" % (job_id, job_name))
        logging.error(s)
        print("执行定时任务失败[job_id=%s，job_name=%s]" % (job_id, job_name))
        print(s)

    # 记录执行完成标志及情况
    success = 1
    if return_code == -1:
        if return_str == "":
            return_str = "提示信息为空"
        logging.error("执行定时任务报错[job_id=%s，job_name=%s]" % (job_id, job_name))
        logging.error(return_str)
        print("执行定时任务报错[job_id=%s，job_name=%s]" % (job_id, job_name))
        print(return_str)
        success = 0

    if return_code == -2:
        if return_str == "":
            return_str = "提示信息为空"
        logging.error("执行定时任务未报错但找不到规定的成功标识文本[job_id=%s，job_name=%s，success_exit=%s]" \
                       % (job_id, job_name, success_exit))
        logging.error(return_str)
        print("执行定时任务未报错但找不到规定的成功标识文本[job_id=%s，job_name=%s，success_exit=%s]" \
                       % (job_id, job_name, success_exit))
        print(return_str)
        success = 0

    if success == 1:
        logging.info("执行job结束：[job_id=%s，job_name=%s]" % (job_id, job_name) + "，执行成功！")
        print("执行job结束：[job_id=%s，job_name=%s]" % (job_id, job_name) + "，执行成功！")
    elif success == 0:
        logging.info("执行job结束：[job_id=%s，job_name=%s]" % (job_id, job_name) + "，执行失败！详情请查看日志文件！")
        print("执行job结束：[job_id=%s，job_name=%s]" % (job_id, job_name) + "，执行失败！详情请查看日志文件！")

def job_python(command, input_param, success_exit):
    '''
    运行类型为python的程序命令，无需在命令中加上python
    :param command: 运行的命令，一般来讲为python文件的路径
    :param input_param: 如果python命令调用需要带参数，可以写到这里
    :param success_exit: 成功标识，若有的话会检测在运行过程中是否有输出成功标识的
    :return: 返回第一个元素为return_code返回编码，第二个元素为return_str返回文本
    '''
    if input_param is None:
        cmd = 'python \"%s\"' % command
    else:
        cmd = 'python \"%s\" %s' % (command, input_param)
    logging.debug("运行的命令为：" + cmd)
    print("运行的命令为：" + cmd)
    try:
        sub = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out, err = sub.communicate()
        # 查看输出内容测试
        # print('out：', out)
        # print('err：', err)
        if err is not None or err != "":
            logging.error(err)
        returncode = sub.returncode
        return_code = 0
        return_str = "执行成功"
        # 程序执行过程中抛出异常
        if returncode != 0:
            return_code = -1
            return_str = err
        elif out is not None and out != "" and success_exit is not None and success_exit != "":
            if out.find(success_exit) == -1:
                # 执行过程的输出中未找到执行成功的限定标识
                return_code = -2
                return_str = out
        elif (out is None or out == "") and (success_exit is not None and success_exit != ""):
            # 未有输出内容但有设置成功文本
            return_code = -2
            return_str = ""
    finally:
        # 判断如果sub变量存在则删除否则不操作
        if 'sub' in dir():
            sub.stdout.close()
            sub.stdout.close()
            del sub
    return return_code, return_str

    return_code = 0
    return_str = "执行成功"
    return return_code, return_str

def job_cmd(command, success_exit):
    '''
    运行类型为cmd的程序命令，即直接在cmd命令提示符中执行的命令
    :param command: 在cmd中运行的命令
    :param success_exit: 成功标识，若有的话会检测在运行过程中是否有输出成功标识的
    :return: 返回第一个元素为return_code返回编码，第二个元素为return_str返回文本
    '''
    logging.debug("运行的命令为：" + command)
    print("运行的命令为：" + command)
    try:
        sub = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        sub.wait()

        err = []
        for line in sub.stderr.readlines():
            err.append(line)
        if len(err) > 0:
            return_code = -1
            return_str = '\r\n'.join(err)
            logging.error(return_str)
        else:
            out = []
            all_output = sub.stdout.readlines()
            for line in all_output:
                out.append(line)
            if all_output.find(success_exit) == -1:
                # 没找到成功标识
                return_code = -2
                return_str = '\r\n'.join(out)
            else:
                # 运行成功
                return_code = 0
                return_str = "执行成功"
    finally:
        # 判断如果sub变量存在则删除否则不操作
        if 'sub' in dir():
            sub.stdout.close()
            sub.stderr.close()
            del sub

    return return_code, return_str

def my_getalljobs(flag):
    '''
    获取当下所有在调度器中的job信息
    :param flag: 传入1为详细信息，传入2为简略信息，仅展示id和name
    '''
    jobs = scheduler.get_jobs()
    if jobs:
        print("已找到调度器中的所有jobs信息如下：")
        print('-' * 40)
        for job in jobs:
            job_info = scheduler.get_job(job.id)
            if job_info.next_run_time is None:
                logging.info("【该job在调度器中已被暂停】")
                print("【该job在调度器中已被暂停】")
            print('id：', job_info.id)
            print('name[任务名]：', job_info.name)
            if flag == '1':
                print('trigger[触发器]：', job_info.trigger)
                print('next_run_time[下一次运行时间]：', job_info.next_run_time)
                print('coalesce[积攒的任务是否只跑一次]：', job_info.coalesce)
                print('max_instances[实例最大并发数]：', job_info.max_instances)
                print('misfire_grace_time[任务超时多少秒后不再重跑]：', job_info.misfire_grace_time)
                print('executor[执行器名]：', job_info.executor)
                print('func_ref[函数调用信息]：', job_info.func_ref)
                print('kwargs[job执行传入的字典]：', job_info.kwargs)
                print('args[job执行传入的参数]：', job_info.args)
            print('-' * 40)
    else:
        print("调度器目前没有job")
        logging.info("调度器目前没有job")


def my_exit():
    '''
    退出中控台的代码
    '''
    try:
        # 非异常情况，尝试等待调度器结束，再终止程序
        scheduler.shutdown(wait=True)
    except Exception as e:
        print("退出中控台结束程序报错：", e)
        logging.error("退出中控台结束程序报错：" + str(e))
    # 退出程序
    print("程序已退出！感谢您的使用！")
    os._exit(0)

if __name__ == '__main__':
    # 中控台启动后的运行代码

    # 将当前运行的cmd程序标题重命名
    os.system("title xjobs定时调度程序")
    print("现在的时间是：%s" % get_format_time())
    print("xjobs定时调度程序已启动，正在初始化...")

    # 定义数据库
    database_path = 'xjobs.db'

    # 日志设置
    log_time = get_format_time(format='%Y%m%d%H%M%S')
    # print(log_time)
    log_foldername = "xjobs_log"
    if not(os.path.exists(log_foldername)):
        os.mkdir(log_foldername)
    log_filename = log_foldername + '\\log_' + log_time + '.log'
    log_level = logging.DEBUG
    # log_level = logging.INFO
    logging.basicConfig(level=log_level,
                        # format='[%(asctime)s] - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        format='[%(asctime)s] - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=log_filename,
                        filemode='w')
    logging.getLogger('apscheduler').setLevel(log_level)
    logging.info("现在的时间是：%s" % get_format_time())
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
                my_pausejobs(s_cmd)
            elif s_cmd.find('resume_job ') > -1:
                my_resumejobs(s_cmd)
            elif s_cmd.find('get_job ') > -1:
                my_getjobs(s_cmd)
            elif s_cmd == "reloadTask" or s_cmd == "6":
                load_task(1)
            elif s_cmd == "updateTask" or s_cmd == "7":
                load_task(0)
            elif s_cmd.find('get_all_jobs ') > -1:
                flag = s_cmd.replace('get_all_jobs', "").strip()
                if flag != '1' and flag != '0':
                    pass
                else:
                    my_getalljobs(flag)
            elif s_cmd == "quit" or s_cmd == "9":
                my_exit()
            else:
                print("无法处理该命令，请重新输入！")
        except Exception as e:
            s = traceback.format_exc()
            print("中控台执行报错，错误信息为：\n" + s)
            logging.error("中控台执行报错，错误信息为：\n" + s)