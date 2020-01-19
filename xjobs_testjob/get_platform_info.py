# coding: utf-8
# Author：雪山凌狐
# website：http://www.xueshanlinghu.com
# version： 1.0
# update_date：2020-01-19

# 一个可以展示系统信息的小脚本，部分源码源自网络

import time
import platform

print("现在的时间是：", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
print('系统类型：', platform.system())
print('操作系统名称及版本号：', platform.platform())
print('操作系统版本号：', platform.version())
print('操作系统的位数：', platform.architecture())
print('计算机硬件架构：', platform.machine())
print('计算机的网络名称：', platform.node())
print('计算机处理器信息', platform.processor())
print()