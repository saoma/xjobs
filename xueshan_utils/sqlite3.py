#coding: utf-8
#Author：雪山凌狐
#website：http://www.xueshanlinghu.com
#鸣谢：boxker

# sqlite3数据库的操作包

import sqlite3

class xsSqlite3():
    '''
    雪山凌狐sqlite3封装工具类
    为了方便调用python中的sqlite3做交互而编写
    '''

    def __init__(self, filename = ":memory"):
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

    def execute(self, sql, param = None):
        '''
        执行数据库的增、删、改操作
        :param sql:执行的sql语句
        :param param: 执行sql的参数数据，比如要insert的数据，可以是list或tuple，默认为None。
        执行单条则传入tuple即可，执行多条则传入list，元素为每条的tuple
        :return: 返回是否执行成功，成功返回True；执行后影响条数为0或执行失败都会返回False
        '''
        count = 0
        try:
            if param is None:
                self.conn.execute(sql)
            else:
                if type(param) is list:
                    self.c.cxecutemany(sql, param)
                else:
                    self.c.execute(sql, param)
            count = self.conn.total_changes
            self.conn.commit()
        except Exception as e:
            print("sqlite3数据库类执行sql语句报错：", e)
            return False, e
        if count > 0:
            return True
        else:
            return False

    def query(self, sql, param = None):
        '''
        数据库查询
        :param sql:查询sql语句
        :param param:sql语句参数，默认为None
        :return:返回查询语句查询后的fetchall结果，返回一个list，如果查不到，则返回空列表
        '''
        if param is None:
            self.c.execute(sql)
        else:
            self.c.execute(sql, param)
        return self.c.fetchall()
