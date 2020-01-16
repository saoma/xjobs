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
        :param param: 执行sql的参数数据，比如要insert的数据，可以是list或tuple，默认为None
        :return: 返回是否执行成功，成功返回True；执行后影响条数为0或执行失败都会返回False
        '''
        pass
