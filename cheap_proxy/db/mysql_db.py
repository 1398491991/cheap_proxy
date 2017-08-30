#coding=utf8
"""
@author: lshu
@file: msdb.py
@time: 2017/8/27 12:44
@desc: 
"""
from ..util.misc import import_module_from_str
import logging
import pprint

logger = logging.getLogger(__name__)

class MysqlDb(object):



    def __init__(self,setting_manager):
        self.setting_manager = setting_manager
        self.setup_conn()
        self.setup_table_name()
        self.create_table()


    @property
    def conn(self):
        return self._conn

    @property
    def store_table_name(self):
        return self._store_table_name


    def setup_table_name(self):
        self._store_table_name = self.setting_manager['STORE_TABLE_NAME']
        logger.info('STORE_TABLE_NAME :%s'%self._store_table_name)


    def setup_conn(self):
        conn_class_path = self.setting_manager['STORE_CONN_CLASS']
        store_conn_config = self.setting_manager['STORE_CONN_CONFIG']
        logger.info('STORE_CONN_CLASS :%s'%conn_class_path)
        logger.info('STORE_CONN_CONFIG :\n%s'%pprint.pformat(store_conn_config))
        self._conn = import_module_from_str(conn_class_path)(**store_conn_config)


    @classmethod
    def from_setting_manager(cls,setting_manager):
        return cls(setting_manager)


    def create_table(self):
        # 表不存在 则创建新表
        try:
            with self.conn.cursor() as cur:
                cur.execute('SELECT 1 FROM `%s`;'%self.store_table_name)
                self.conn.commit()

        except:
            sql = """
            CREATE TABLE `%s` (
              `proxy` varchar(30) NOT NULL,
              `test_times` int(5) NOT NULL DEFAULT '0',
              `failure_times` int(5) NOT NULL DEFAULT '0',
              `success_rate` float(5,2) NOT NULL DEFAULT '0.00',
              `avg_response_time` float NOT NULL DEFAULT '0',
              `score` float(5,2) NOT NULL DEFAULT '0.00',
              PRIMARY KEY (`proxy`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """%self.store_table_name
            logger.info('create table :%s' % self.store_table_name)
            logger.info('run sql :\n%s'%sql)
            with self.conn.cursor() as cur:
                cur.execute(sql)
                self.conn.commit()



    def get_all(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute('select * from %s'%self.store_table_name)
                result = cur.fetchall()
                self.conn.commit()
            return result

        except:
            # 表不存在
            return []



    def exist(self,proxy):
        with self.conn.cursor() as cur:
            count = cur.execute('select 1 from %s WHERE proxy="%s"'%(self.store_table_name,proxy),)
            self.conn.commit()
        return bool(count)

    def save_proxy(self,proxy):
        if proxy.from_store:
            # 来自数据库 则 直接更新 但这有可能因为 其他进程删除这个代理 是的这个sql执行错误
            sql = 'update '+self.store_table_name+' set test_times=%s,failure_times=%s,success_rate=%s,' \
                                                  'avg_response_time=%s,score=%s where proxy="%s"'%(proxy.test_times,
                    proxy.failure_times,proxy.success_rate,
                    proxy.avg_response_time,proxy.score,proxy)
            data = None


        else:
            # 来自网站 执行插入操作, 这回因为代理的唯一索引而导致错误
            sql = 'insert into '+self.store_table_name+' VALUES (%s,%s,%s,%s,%s,%s)'
            data = (str(proxy),proxy.test_times,
                    proxy.failure_times,proxy.success_rate,
                    proxy.avg_response_time,proxy.score,)

        try:
            with self.conn.cursor() as cur:
                cur.execute(sql,data)
                self.conn.commit()

        except:
            pass
            # logger.exception('proxy %s to store error'%proxy)

        else:
            logger.debug('proxy %s to store succeed'%proxy)


