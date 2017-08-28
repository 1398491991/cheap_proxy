#coding=utf8
"""
@author: lshu
@file: redis.py
@time: 2017/8/27 12:45
@desc: 
"""
from ..util.misc import import_module_from_str
import logging
import pprint

logger = logging.getLogger(__name__)

class RedisDb(object):

    def __init__(self,setting_manager):
        self.setting_manager = setting_manager
        self.setup_conn()

    @property
    def conn(self):
        return self._conn

    def setup_conn(self):
        conn_class_path = self.setting_manager['QUEUE_CONN_CLASS']
        conn_config = self.setting_manager['QUEUE_CONN_CONFIG']
        logger.info('QUEUE_CONN_CLASS :%s'%conn_class_path)
        logger.info('QUEUE_CONN_CONFIG :\n%s'%pprint.pformat(conn_config))
        conn_class = import_module_from_str(conn_class_path)
        self._conn = conn_class(**conn_config)

    @classmethod
    def from_setting_manager(cls,setting_manager):
        return cls(setting_manager)