#coding=utf8
"""
@author: lshu
@file: proxy.py
@time: 2017/8/27 13:30
@desc: 
"""
import re


_proxy_re_compile = re.compile('^http[s]{0,1}://(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9]):\d+$')

def safe_proxy(proxy_str):
    # 'http://127.0.0.1:80'
    try:
        _proxy_re_compile.match(proxy_str).group()

    except AttributeError:
        return False

    else:
        return True



class Proxy(object):
    def __init__(self,host,port,pt,**kwargs):
        self._host = host
        self._port = port
        self._pt = pt


    def __str__(self):
        return '%s://%s:%s'%(self._pt,self._host,self._port)

    def is_safe_proxy(self):
        return safe_proxy(self.__str__())

    def serialize(self):
        # http://127.0.0.1:80
        return self.__str__()

    @staticmethod
    def deserialize(s,):
        # ('http', '127.0.0.1', '80')
        pt,host,port = re.match('^(http[s]{0,1})://(\d+\.\d+\.\d+\.\d+):(\d+)$', s).groups()
        return Proxy(host,port,pt)
