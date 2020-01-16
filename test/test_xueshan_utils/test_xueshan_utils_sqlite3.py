# coding: utf-8
# Author：雪山凌狐
# website：http://www.xueshanlinghu.com
# version： 1.0
# update_date：2020-01-16

# 测试雪山共同类的sqlite3类

from os.path import abspath, dirname
project_path = dirname(dirname(dirname(abspath(__file__))))
import sys
sys.path.append(project_path)

import xueshan_utils as xs_utils

# 初始化内存数据库
sqlite = xs_utils.xsSqlite3()

# 建表测试
res, m = sqlite.execute("create table test (id int not null, name text, age int)")
print(res, m)
# 表多条插入测试
res, m = sqlite.execute("insert into test(id,name,age) values (?,?,?)", [(3, "王五", 20), (4, "郑六", 22)])
print(res, m)
# 表查询测试
res = sqlite.query("select * from test")
print("test表查询结果：", res)
# 表删除测试
res, m = sqlite.execute("drop table test")
print(res, m)

# 数据库断开连接
sqlite.close_all()

