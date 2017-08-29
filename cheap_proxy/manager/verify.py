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
from requests.exceptions import RequestException
import time

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
        proxy = self.proxy_class(**proxy) # 实例化一个代理对象 根据 dict
        proxy.test_times_increment() # 测试次数 +1

        test_result,use_time = self.test_request(proxy)
        logger.debug('test request use %s done,result %s ,use time %s'%(proxy,test_result,use_time))
        if not test_result:
            proxy.failure_times_increment() # 失败次数 +1

        proxy.set_new_response_time(use_time) # 设置本次所用的时间
        return self.to_store(proxy)


    def test_request(self,proxy):
        test_result = False
        start_time = time.time()
        try:
            # 超过40秒的代理算失败
            r = requests.get('https://www.baidu.com', proxies=proxy.to_requests_format(), timeout=40, verify=False)
            if r.status_code == 200:
                logger.debug('%s is ok' % proxy)
                test_result = True

        except RequestException:
            logger.error('%s is failed'%proxy)


        end_time = time.time()

        return (test_result,end_time - start_time)


    def to_store(self,proxy):
        logger.debug('new proxy to store :%s'%proxy)
        self.store_db.save_proxy(proxy)

