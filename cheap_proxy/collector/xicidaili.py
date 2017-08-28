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

    @classmethod
    def from_setting_manager(cls,setting_manager):
        return cls(setting_manager)

    @property
    def proxy_class(self):
        if not hasattr(self,'_proxy_class'):
            self._proxy_class = import_module_from_str(self.setting_manager.get('PROXY_CLASS', 'cheap_proxy.util.proxy.Proxy'))

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
