#!/usr/bin/python
# coding:utf-8

from Global import default
from Credentials import Credentials
from Common import Common


class DB:
    '''
    The class is about database things.
    The functions connect(),running_query() in this class are the static funtion,you can use it directly.
    Example:
            con,cur = DB.connect()
    '''

    def __init__(self):
        self.con = None
        self.cur = None
        import pymysql
        self.pymysql = pymysql

    def connect(self, host='db.base-fx.com', city=default['city'],user='',passwd='',port=3306):
        import pymysql.cursors
        self.city = city.upper()
        hosts = {
            'BJ': {'qube': 'qube.bj.base-fx.com'},
            'DC': {'qube': 'qube.dc.base-fx.com'},
            'WX': {'qube': 'qube.wx.base-fx.com'},
            'XM': {'qube': 'qube.xm.base-fx.com'},
            'KL': {'qube': 'qube.kl.base-fx.com'},
        }
        try:
            host = hosts[self.city][host]
        except:
            pass
        if not user and not passwd:
            user, passwd = Credentials(host, self.city)
        con = self.pymysql.connect(host, user, passwd, charset='utf8', cursorclass=pymysql.cursors.DictCursor,
                                   connect_timeout=30, use_unicode=True,port=port)
        cur = con.cursor()
        return con, cur

    def connection(self,**kwargs):
        """
        :param kwargs: host='db.base-fx.com', city=default['city'],user='',passwd='',port=3306
        :return: mysql connection
        """
        if self.con:
            return  self.con
        else:
            kwargs.get('host','db.base-fx.com')
            kwargs.get('city', default['city'])
            kwargs.get('user', '')
            kwargs.get('password', '')
            kwargs.get('port', 3306)
            self.con,self.cur = self.connect(**kwargs)
            return self.con


    def cursor(self,**kwargs):
        """
        :param kwargs: host='db.base-fx.com', city=default['city'],user='',passwd='',port=3306
        :return: mysql cursor
        """
        if self.cur:
            return self.cur
        else:
            self.connection(**kwargs)
            return self.cur


    def big_query(self, con, cur, query, data, limit_number=5000, debug=False):
        '''
        Change large number data of database,for insert、updata、delete.
        con--connection.
        cur--cursor.
        query--string.
        data--list ,it contains tuples,like [(1,'Tom'),(2,'Jack'),...].
        limit_number:int,the number of the query changes per times.
        debug--bool, True: print the running tips; Flase: print nothing.
        Example:
                con,cur = DB.connect()
                query ="INSERT INTO `test`.`user` (`id`,`name`) VALUES (%s,%s)"
                data = [(1,'Tom'),(2,'Jack')]
                running_query(con,cur,query,data)
        '''
        common = Common(debug=debug)
        data_current = []
        count = 0
        common.msg('Start to change data...\nTotal:%s' % len(data))
        for datum in data:
            count += 1
            data_current.append(datum)
            # [TIP]--Per limit_number rows to execute query once,or it's the last part--
            if len(data_current) % limit_number == 0 or count == len(data):
                cur.executemany(query, data_current)
                common.msg('Current change data:%s' % count)
                data_current = []
                # [NOTE]--You can commit later,but I think it's better here,especialy changing data more than 10000 rows--
                con.commit()
        # con.commit() #[NOTE]--Yes,I commited here before ,but it's disgusting when you break by some thing--
        common.msg('Change over!')

    def connect_db(self, hash):
        import pymysql.cursors
        con = self.pymysql.connect(hash['Host'], hash['User'], hash['Password'],
                                   charset=hash['CharSet'],
                                   cursorclass=pymysql.cursors.DictCursor,
                                   connect_timeout=hash['Timeout'],
                                   db=hash['Database'])
        cur = con.cursor()
        return con, cur
