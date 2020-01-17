# coding: utf-8
# Author：雪山凌狐
# website：http://www.xueshanlinghu.com
# version： 1.0
# update_date：2020-01-17

# 测试一下traceback的报错输出是长什么样的

import traceback

# 尝试运行一个会报错的内容来
try:
    "111".to_lower()
except Exception as e:
    print("报错信息为：", e)
    print("traceback报错信息为：", traceback.format_exc())
