# coding: utf-8
# Author：雪山凌狐
# website：http://www.xueshanlinghu.com
# version： 1.0
# update_date：2020-01-23

# 测试获取文件夹中修改日期最晚的文件名

import os

def get_latest_log_filename(log_foldername):
    '''
    获取修改时间最晚的一份log的文件名并返回
    :param log_foldername: log日志存放的文件夹名
    :return: log文件名字符串，包含后缀名
    '''
    # 因为本测试文件在比较里面，所以取上几级目录的内容
    project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    folder_path = project_path + "\\" + log_foldername
    print(folder_path)
    all_filenames = os.listdir(folder_path)
    final_filename = ''
    final_st_mtime = float(0)
    for per_filename in all_filenames:
        whole_file_path = folder_path + "\\" + per_filename
        print(whole_file_path)
        statinfo = os.stat(whole_file_path)
        # 取修改时间，这是一个浮点数
        print(statinfo.st_mtime)
        if statinfo.st_mtime >= final_st_mtime:
            final_st_mtime = statinfo.st_mtime
            final_filename = per_filename
    print("最后修改的文件名为：" + final_filename)
    return final_filename


if __name__ == '__main__':
    foldername = "xjobs_log"
    get_latest_log_filename(foldername)