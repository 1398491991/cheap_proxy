#coding=utf8
"""
@author: lshu
@file: verify.py
@time: 2017/8/27 12:49
@desc: 
"""

import requests
from ..util.misc import import_module_from_str
from .crawl import CrawlManager
import logging

logger = logging.getLogger(__name__)

class VerifyManager(CrawlManager):

    def __init__(self,setting_manager):
        super(VerifyManager,self).__init__(setting_manager)
        self.setup_store_db()
        self.setup_proxy_class()

    @property
    def store_db(self):
        return self._store_db

    @property
    def proxy_class(self):
        return self._proxy_class


    def setup_store_db(self):

        store_db_class_path = self.setting_manager['STORE_DB_CLASS']
        logger.info('STORE_DB_CLASS :%s'%store_db_class_path)
        store_db_class = import_module_from_str(store_db_class_path)
        self._store_db = store_db_class.from_setting_manager(self.setting_manager)

    def setup_proxy_class(self):
        proxy_class_path = self.setting_manager['PROXY_CLASS']
        logger.info('PROXY_CLASS :%s' % proxy_class_path)
        self._proxy_class = import_module_from_str(proxy_class_path)

    def get_parallel_size(self):
        # 计算合适的处理池大小
        size = self.setting_manager['VERIFY_PARALLEL_SIZE']
        logger.info('VERIFY_PARALLEL_SIZE :%s'%size)
        return size


    def run(self):
        self.collector_pool.map(self.map_run, self.raw_proxy_queue)


    def map_run(self,proxy):
        proxy = self.proxy_class(**proxy)
        proxies = proxy.to_requests_format()
        proxy.test_times_increment()
        try:
            # 超过40秒的代理就不要了
            r = requests.get('https://www.baidu.com', proxies=proxies, timeout=40, verify=False)
            if r.status_code == 200:
                logger.debug('%s is ok' % proxies)

        except:
            logger.error('proxy error %s'%proxies)
            proxy.failure_times_increment()

        proxy.set_new_response_time(1)
        return self.to_store(proxy)

    def to_store(self,proxy):
        logger.debug('new proxy to store :%s'%proxy)
        self.store_db.save_proxy(proxy)

