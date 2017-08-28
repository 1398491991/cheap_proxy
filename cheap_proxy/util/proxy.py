#coding=utf8
"""
@author: lshu
@file: proxy.py
@time: 2017/8/27 13:30
@desc: 
"""
import re
import scrapy_redis

_proxy_re_compile = re.compile('^http[s]{0,1}://(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9]):\d+$')

def safe_proxy(proxy_str):
    # 'http://127.0.0.1:80' 判断格式是否正确
    try:
        _proxy_re_compile.match(proxy_str).group()

    except AttributeError:
        return False

    else:
        return True



class Proxy(object):
    def __init__(self,host,port,pt,
                 test_times = 0,
                 failure_times = 0,
                 success_rate = 0,
                 avg_response_time = None,
                 score = None,
                 **kwargs):

        self.host = host
        self.port = port
        self.pt = pt # http or https

        self._test_times = test_times
        self._failure_times = failure_times
        self._success_rate = success_rate
        self._avg_response_time = avg_response_time
        self._score = score


    def __str__(self):
        return '%s://%s:%s'%(self.pt,self.host,self.port)

    __repr__ = __str__


    def is_safe_proxy(self):
        return safe_proxy(self.__str__())


    def to_requests_format(self):
        return {self.pt:self.__str__()}

    def to_base_dict(self):
        return {'host':self.host,
                'port':self.port,
                'pt': self.pt,}

    def to_dict(self):
        return {'host':self.host,
                'port':self.port,
                'pt': self.pt,
                'test_times': self.test_times,
                'failure_times': self.failure_times,
                'success_rate': self.success_rate,
                'avg_response_time': self.avg_response_time,
                'score': self.score,
                }


    def test_times_increment(self,v = 1):
        self._test_times += v

    def failure_times_increment(self, v=1):
        # 失败自增
        self._failure_times += v


    def set_new_response_time(self,new_response_time):
        # 根据最新一次的结果返回计算结果
        if self.avg_response_time is None:
            self._avg_response_time = new_response_time

        else:
            self._avg_response_time = ((self._avg_response_time * self._test_times) + new_response_time) / (self._test_times + 1)


    @property
    def score(self):
        return (self.success_rate + self.test_times / 500) / self.avg_response_time


    @property
    def failure_times(self):
        return self._failure_times

    @property
    def test_times(self):
        return self._test_times

    @property
    def avg_response_time(self):
        return self._avg_response_time

    @property
    def success_rate(self):
        try:
            return 1.0 - float(self._failure_times) / self.test_times
        except ZeroDivisionError:
            return 0