#!/usr/bin/env python
#coding=utf-8

"""
@author: lshu
@file: crawl.py
@time: 2017-08-28 14:42
@desc: 
"""


from ..util.misc import import_module_from_str
import logging


logger = logging.getLogger(__name__)


class CrawlManager(object):


    def __init__(self,setting_manager):
        self.setting_manager = setting_manager
        self.setup_raw_proxy_queue()
        self.setup_parallel_pool()

    @classmethod
    def from_setting_manager(cls,setting_manager):
        return cls(setting_manager)


    def setup_raw_proxy_queue(self):

        raw_queue_class_path = self.setting_manager['RAW_QUEUE_CLASS']
        raw_queue_key = self.setting_manager['RAW_QUEUE_KEY']
        raw_db_class_path = self.setting_manager['RAW_DB_CLASS']
        serialize_path = self.setting_manager['SERIALIZE']
        deserialize_path = self.setting_manager['DESERIALIZE']
        verify_idle_time_out = self.setting_manager['VERIFY_IDLE_TIME_OUT']
        logger.info('RAW_QUEUE_CLASS :%s'%raw_queue_class_path)
        logger.info('RAW_QUEUE_KEY :%s'%raw_queue_key)
        logger.info('RAW_DB_CLASS :%s'%raw_db_class_path)
        logger.info('SERIALIZE :%s'%serialize_path)
        logger.info('DESERIALIZE :%s'%deserialize_path)
        logger.info('VERIFY_IDLE_TIME_OUT :%s'%verify_idle_time_out)

        server = import_module_from_str(raw_db_class_path).from_setting_manager(self.setting_manager)
        serialize = import_module_from_str(serialize_path)
        deserialize = import_module_from_str(deserialize_path)

        self._raw_proxy_queue = import_module_from_str(raw_queue_class_path)(server,
                                                                             raw_queue_key,
                                                                             serialize,
                                                                             deserialize,
                                                                             verify_idle_time_out)

    @property
    def raw_proxy_queue(self):
        return self._raw_proxy_queue


    @property
    def collector_pool(self):
        return self._collector_pool


    def get_parallel_size(self):
        # 计算合适的处理池大小
        raise NotImplemented

    def setup_parallel_pool(self):
        size = self.get_parallel_size()
        collector_pool_class_path = self.setting_manager['COLLECTOR_POOL_CLASS']
        logger.info('COLLECTOR_POOL_CLASS :%s'%collector_pool_class_path)
        self._collector_pool = import_module_from_str(collector_pool_class_path)(size)

    def run(self):
        raise NotImplemented


    def map_run(self,x):
        raise NotImplemented
