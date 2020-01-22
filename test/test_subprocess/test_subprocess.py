# coding: utf-8
# Author：雪山凌狐
# website：http://www.xueshanlinghu.com
# version： 1.0
# update_date：2020-01-22

# 测试一下如何使用subprocess库

import subprocess

def run_python(python_path):
    cmd = "python %s" % python_path
    print("运行的命令为：" + cmd)
    try:
        # 结论：通过添加text=True命令，可使返回的结果为string而不是byte，方便后续调用和查看
        sub = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out, err = sub.communicate()
        returncode = sub.returncode
        return_code = 0
        return_str = "执行成功"
        # 程序执行过程中抛出异常
        if returncode != 0:
            return_code = -1
            return_str = err
        if out.find("操作系统") == -1:
            return_code = -2
            return_str = "找不到操作系统几个字"
        # 进行输出测试
        print("out:", out)
        print("err:", err)

    finally:
        if 'sub' in dir():
            sub.stdout.close()
            sub.stdout.close()
            del sub
    return return_code, return_str


if __name__ == "__main__":
    python_file = "get_platform_info.py"
    return_code, return_str = run_python(python_file)
    print(return_code, return_str)