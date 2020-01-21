# coding: utf-8
# Author：雪山凌狐
# website：http://www.xueshanlinghu.com
# version： 1.0
# update_date：2020-01-21

# 测试一下如何使用subprocess库

import subprocess

def run_python(python_path):
    cmd = "python %s" % python_path
    print("运行的命令为：" + cmd)
    try:
        sub = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = sub.communicate()
        sub.stdout.close()
        sub.stdout.close()
        returncode = sub.returncode
        return_code = 0
        return_str = "执行成功"
        # 程序执行过程中抛出异常
        if returncode != 0:
            return_code = -1
            return_str = err

        # 进行输出测试
        print("out:", out)
        print(out.decode("gbk"))

    finally:
        if 'sub' in dir():
            del sub
    return return_code, return_str


if __name__ == "__main__":
    python_file = "get_platform_info.py"
    return_code, return_str = run_python(python_file)
    print(return_code, return_str)