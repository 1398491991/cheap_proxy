#coding=utf8
"""
@author: lshu
@file: verify.py
@time: 2017/8/27 12:49
@desc: 
"""
import requests
from requests.exceptions import RequestException
import time
import logging


# 一个默认的测试代理IP是否可用的类

logger = logging.getLogger(__name__)

class VerifyProxy(object):

    def __init__(self,setting_manager):
        self.setting_manager = setting_manager

    @classmethod
    def from_setting_manager(cls,setting_manager):
        return cls(setting_manager)


    def verify_proxy(self,proxy):
        # 根据请求的 proxy 实例 返回 请求状态 和 耗时
        # 默认的 class
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