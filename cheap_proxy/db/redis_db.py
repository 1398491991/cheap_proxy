#coding=utf8
"""
@author: lshu
@file: redis.py
@time: 2017/8/27 12:45
@desc: 
"""
from ..util.misc import import_module_from_str

class RedisDb(object):

    def __init__(self,setting_manager):
        self.setting_manager = setting_manager

    @property
    def conn(self):
        if not hasattr(self,'_conn'):
            self._conn = self.make_conn()

        return self._conn

    def make_conn(self):
        conn_class = import_module_from_str(self.setting_manager.get('QUEUE_CONN_CLASS','redis.Redis'))
        return conn_class(**self.setting_manager.get('QUEUE_CONN_CONFIG',{}))

    @classmethod
    def from_setting_manager(cls,setting_manager):
        return cls(setting_manager)