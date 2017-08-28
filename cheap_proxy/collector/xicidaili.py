#coding=utf8
"""
@author: lshu
@file: xicidaili.py
@time: 2017/8/27 13:20
@desc: 
"""
import requests
from lxml import etree
from ..util.misc import import_module_from_str

class Xicidaili(object):

    def __init__(self,setting_manager):
        self.setting_manager = setting_manager
        self._set_proxy_class()

    @classmethod
    def from_setting_manager(cls,setting_manager):
        return cls(setting_manager)

    def _set_proxy_class(self):
        proxy_class_path = self.setting_manager['PROXY_CLASS']
        self._proxy_class = import_module_from_str(proxy_class_path)

    @property
    def proxy_class(self):
        return self._proxy_class


    def crawl(self):
        response = requests.get('http://www.xicidaili.com/nn',
                                headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'})
        e = etree.HTML(response.text)
        odds = e.xpath('//tr[@class="odd"]')
        for odd in odds:
            host,port,_,_,_,pt = odd.xpath('.//td/text()')[:6]
            proxy = self.proxy_class(host,port,pt.lower())
            if proxy.is_safe_proxy():
                yield proxy
