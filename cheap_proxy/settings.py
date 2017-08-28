#coding=utf8
"""
@author: lshu
@file: settings.py
@time: 2017/8/27 12:44
@desc: 
"""

COLLECTORS = {'cheap_proxy.collector.xicidaili.Xicidaili':True,
              }

QUEUE_CONN_CLASS = 'redis.Redis'

QUEUE_CONN_CONFIG = {'host':'localhost',
                     'port':6379,
                     'db':0,
                     }


RAW_QUEUE_CLASS = 'cheap_proxy.queue.redis_queue.RedisQueue'
RAW_QUEUE_KEY = 'cheap_proxy:raw_proxy'
RAW_DB_CLASS = 'cheap_proxy.db.redis_db.RedisDb'
VERIFY_IDLE_TIME_OUT = 10


COLLECTOR_PARALLEL_SIZE = 3
VERIFY_PARALLEL_SIZE = 5

COLLECTOR_POOL_CLASS = 'gevent.pool.Pool'

PROXY_CLASS = 'cheap_proxy.util.proxy.Proxy'


SERIALIZE = 'cheap_proxy.util.jsoncompat.dumps'
DESERIALIZE = 'cheap_proxy.util.jsoncompat.loads'

STORE_CONN_CLASS = 'pymysql.Connect'

STORE_CONN_CONFIG = {
                    'host':'192.168.1.106',
                    'port' : 3306,
                    'user':'root',
                    'passwd':'123456789',
                    'charset':'utf8',
                    'db': 'lshu',
                    }

STORE_TABLE_NAME = 'cheap_proxy'

STORE_DB_CLASS = 'cheap_proxy.db.mysql_db.MysqlDb'
