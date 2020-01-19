# coding: utf-8
# Author：雪山凌狐
# website：http://www.xueshanlinghu.com
# version： 1.0
# update_date：2020-01-18
# 鸣谢：boxker

# sqlite3数据库的操作包

import sqlite3


class xsSqlite3():
    '''
    雪山凌狐sqlite3封装工具类
    为了方便调用python中的sqlite3做交互而编写
    '''

    def __init__(self, filename=":memory:"):
        '''
        初始化数据库，默认文件名为:memory:，即打开内存数据库。
        如果路径中数据库存在，则会自动创建一个新的数据库。
        :param filename: 文件名（包含后缀名），可以是相对路径或绝对路径
        '''
        self.filename = filename
        self.conn = sqlite3.connect(self.filename)
        self.c = self.conn.cursor()

    def close_conn(self):
        '''
        仅关闭数据库连接
        '''
        self.conn.close()

    def close_cursor(self):
        '''
        仅关闭游标cursor，需在关闭数据库连接之前
        '''
        self.c.close()

    def close_all(self):
        '''
        分别依次关闭游标cursor和数据库连接
        '''
        self.c.close()
        self.conn.close()

    def execute(self, sql, param=None):
        '''
        执行数据库的增、删、改操作，一般建议同一类型的操作才写在一起
        :param sql:执行的sql语句
        :param param: 执行sql的参数数据，比如要insert的数据，可以是list或tuple，默认为None。
        执行单条则传入tuple即可（不要传入list），执行多条则传入list，元素为每条的tuple
        :return: 返回是否执行成功，返回元组，第一个元素为是否成功。
        成功返回True；执行失败会返回False。
        第二个元素为返回的信息，错误信息或成功信息等。
        '''
        count = 0
        try:
            if param is None:
                self.conn.execute(sql)
            else:
                if type(param) is list:
                    self.c.executemany(sql, param)
                else:
                    self.c.execute(sql, param)
            count = self.c.rowcount
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("sqlite3数据库类执行sql语句报错：", e)
            return False, e
        if count > 0:
            # 这里覆盖insert，update，delete操作
            return True, sql[0:sql.find(" ")] + "操作影响行数为：" + str(count)
        elif sql.lower().startswith("create") or sql.lower().startswith("drop"):
            # 这里覆盖建表和删表操作
            return True, sql[0:sql.find(" ")] + " table successful!"
        elif count == 0:
            return True, sql[0:sql.find(" ")] + "操作影响行数为：0"
        else:
            return False, "unknown error"

    def query(self, sql, param=None):
        '''
        数据库查询
        :param sql:查询sql语句
        :param param:sql语句参数，默认为None
        :return:返回查询语句查询后的fetchall结果，返回一个list，如果查不到，则返回空列表。
        如果报错，返回错误提示列表，第一个元素为"query error"字符串，第二个元素为错误信息
        '''
        try:
            if param is None:
                self.c.execute(sql)
            else:
                self.c.execute(sql, param)
        except Exception as e:
            print("sqlite3数据库类运行查询的sql语句报错：", e)
            return ["query error", e]
        return self.c.fetchall()

    def query_cursor(self, sql, param=None):
        '''
        数据库查询，返回游标
        :param sql:查询sql语句
        :param param:sql语句参数，默认为None
        :return:返回查询语句查询后的游标，可以进行迭代遍历，对于返回的结果预计量很大的时候可以使用
        如果报错，打印错误信息，仍然可以返回空游标
        '''
        try:
            if param is None:
                self.c.execute(sql)
            else:
                self.c.execute(sql, param)
        except Exception as e:
            print("sqlite3数据库类运行查询的sql语句报错（cursor)：", e)
        # 无论是否报错都可以返回游标
        return self.c


if __name__ == '__main__':
    # 以下是此类的测试代码

    # 内存数据库读写测试
    # 初始化连接，不传入参数则会自动打开一个内存数据库
    sqlite = xsSqlite3()
    # 正确建表测试
    res, m = sqlite.execute("create table test (id int not null, name text, age int)")
    print(res, m)
    # ×××建表语句错误测试×××
    res, m = sqlite.execute("create table test_error")
    print(res, m)
    # 表单条插入测试
    res, m = sqlite.execute("insert into test(id,name,age) values (?,?,?)", (1, "张三", 18))
    print(res, m)
    # ×××错误的插入示范，单条传入list插入方式会报错×××
    res, m = sqlite.execute("insert into test(id,name,age) values (?,?,?)", [2, "李四", 19])
    print(res, m)
    # 表多条插入测试
    res, m = sqlite.execute("insert into test(id,name,age) values (?,?,?)", [(3, "王五", 20), (4, "郑六", 22)])
    print(res, m)
    # 表查询测试
    res = sqlite.query("select * from test")
    print("test表查询结果：", res)
    res = sqlite.query("select * from test where id=?", (3,))
    print("test表查询结果：", res)
    res = sqlite.query("select * from test where id=?", (5,))
    print("test表查询结果：", res)
    res = sqlite.query_cursor("select * from test")
    for cur_res in res:
        print("test表查询结果（游标遍历）：", cur_res)
    # 表查询的sql语句有误测试
    res = sqlite.query("select * test")
    print("test表查询结果：", res)
    res = sqlite.query_cursor("select * test")
    print("查询报错返回的游标：", res)
    for cur_res in res:
        print("如果看到我这一行提示，说明报错的游标还能取出内容，如果看不到说明取不出")
        print("test表查询结果（游标遍历）：", cur_res)
    # 表更新测试
    res, m = sqlite.execute("update test set age = ? where id = ?", (55, 1))
    print(res, m)
    res = sqlite.query("select * from test")
    print("test表查询结果：", res)
    # 表数据行删除测试
    res, m = sqlite.execute("delete from test where age = ?", (55,))
    print(res, m)
    res = sqlite.query("select * from test")
    print("test表查询结果：", res)
    # 表删除测试
    res, m = sqlite.execute("drop table test")
    print(res, m)

    # 关闭数据库连接
    sqlite.close_all()
