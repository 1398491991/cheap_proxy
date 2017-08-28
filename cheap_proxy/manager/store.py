#!/usr/bin/env python
#coding=utf-8

"""
@author: lshu
@file: store.py
@time: 2017-08-28 17:26
@desc: 历史的代理从新检测
"""
import logging
from .verify import VerifyManager
import re
logger = logging.getLogger(__name__)


class StoreManager(VerifyManager):

    def run(self):
        result = self.store_db.get_all()
        for proxy in result:
            proxy_str,test_times,failure_times,success_rate,avg_response_time,score = proxy
            pt,host,port = re.search('^(http[s]{0,1})://(\d+\.\d+\.\d+\.\d+):(\d+)$',proxy_str).groups()
            proxy = self.proxy_class(host,port,pt,
                                     test_times,
                                     failure_times,
                                     success_rate,
                                     avg_response_time,
                                     score,)
            self.raw_proxy_queue.push(proxy.to_dict())
