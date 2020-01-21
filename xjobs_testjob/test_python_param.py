# coding: utf-8
# Author：雪山凌狐
# website：http://www.xueshanlinghu.com
# version： 1.0
# update_date：2020-01-21

# 测试python传入参数后面多几个空格是否能正常执行

import time
import sys

def get_time_now(aaa):
    print(aaa)
    print(time.localtime())


if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) > 1:
        get_time_now(sys.argv[1])
    else:
        print("没有多余的参数")