#coding=utf8
"""
@author: lshu
@file: verify.py
@time: 2017/8/27 12:49
@desc: 
"""
from ..util.misc import import_module_from_str
import requests
import logging
from ..util.misc import to_native_str

logger = logging.getLogger(__name__)
logging.basicConfig()
class VerifyManager(object):


    def __init__(self, setting_manager):
        self.setting_manager = setting_manager

    @classmethod
    def from_setting_manager(cls, setting_manager):
        return cls(setting_manager)

    def make_raw_proxy_queue(self):
        raw_queue_class_path = self.setting_manager.get('RAW_QUEUE_CLASS', 'cheap_proxy.queue.redis_queue.RedisQueue')
        raw_queue_key = self.setting_manager.get('RAW_QUEUE_KEY', 'cheap_proxy:raw_proxy')
        raw_db_class_path = self.setting_manager.get('RAW_DB_CLASS', 'cheap_proxy.db.redis_db.RedisDb')

        server = import_module_from_str(raw_db_class_path).from_setting_manager(self.setting_manager)
        self._raw_proxy_queue = import_module_from_str(raw_queue_class_path)(server, raw_queue_key)

    @property
    def raw_proxy_queue(self):
        return self._raw_proxy_queue

    def verify(self):
        self.make_raw_proxy_queue()

        while 1:
            obj = self._raw_proxy_queue.pop(3)
            if not obj:
                break

            result = self.verify_proxy(obj)



    @property
    def proxy_class(self):
        if not hasattr(self,'_proxy_class'):
            self._proxy_class = import_module_from_str(self.setting_manager.get('PROXY_CLASS', 'cheap_proxy.util.proxy.Proxy'))

        return self._proxy_class


    def verify_proxy(self,proxy):
        proxies = self.proxy_class.deserialize(to_native_str(proxy))
        proxies = {proxies._pt: "%s"%proxies}
        try:
            # 超过40秒的代理就不要了
            r = requests.get('https://www.baidu.com', proxies=proxies, timeout=40, verify=False)
            if r.status_code == 200:
                logger.debug('%s is ok' % proxies)
                return True

        except:
            logger.info('validUsefulProxy error %s'%proxies)
            return False