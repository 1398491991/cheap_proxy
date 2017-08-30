#coding=utf8
"""
@author: lshu
@file: verify.py
@time: 2017/8/27 12:49
@desc: 
"""


from ..util.misc import import_module_from_str
from .crawl import CrawlManager
import logging


logger = logging.getLogger(__name__)

class VerifyManager(CrawlManager):

    def __init__(self,setting_manager):
        super(VerifyManager,self).__init__(setting_manager)
        self.setup_store_db()
        self.setup_proxy_class()
        self.setup_verify_proxy()

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


    def setup_verify_proxy(self):
        # 验证代理是否可用的方法类 默认调用 verify_proxy 方法
        verify_proxy_class_path = self.setting_manager['VERIFY_PROXY_CLASS']
        logger.info('VERIFY_PROXY_CLASS :%s' % verify_proxy_class_path)
        self.verify_proxy = import_module_from_str(verify_proxy_class_path).from_setting_manager(self.setting_manager)


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

        test_result,use_time = self.verify_proxy.verify_proxy(proxy) # 验证代理是否可用

        logger.debug('test request use %s done,result %s ,use time %s'%(proxy,test_result,use_time))
        if not test_result:
            proxy.failure_times_increment() # 失败次数 +1

        proxy.set_new_response_time(use_time) # 设置本次所用的时间
        return self.to_store(proxy)


    def to_store(self,proxy):
        log_msg = 'old proxy to store :%s'%proxy if proxy.from_store else 'new proxy to store :%s'%proxy
        logger.debug(log_msg)
        self.store_db.save_proxy(proxy)

