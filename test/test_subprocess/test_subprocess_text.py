# coding: utf-8
# Author：雪山凌狐
# website：http://www.xueshanlinghu.com
# version： 1.0
# update_date：2020-01-29

# 测试一下subprocess库没有text属性该如何保证输出内容
# 研究问题：有可能比较旧的python3版本，比如3.6.6，subprocess.Popen没有text属性，怎么办？

import subprocess

def run_python(python_path):
    cmd = "python %s" % python_path
    print("运行的命令为：" + cmd)
    try:
        # 在3.7版本中才添加text参数作为universal_newlines更好理解的别名，若为3.6版本则必须使用universal_newlines
        sub = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        out, err = sub.communicate()
        returncode = sub.returncode
        return_code = 0
        return_str = "执行成功"
        # 程序执行过程中抛出异常
        if returncode != 0:
            print("returncode", returncode)
            return_code = -1
            return_str = err
        if out.find("操作系统") == -1:
            return_code = -2
            return_str = "找不到操作系统几个字"
        else:
            print("找到了标识字符")
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

