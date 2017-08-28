#coding=utf8
"""
@author: lshu
@file: setting.py
@time: 2017/8/27 12:49
@desc: 加载配置文件，合并到默认配置文件
"""
from .. import settings
from importlib import import_module



class SettingManager(object):

    settings = settings.__dict__

    def __init__(self,ext_settings = None):
        self._load_ext_settings(ext_settings)
        self._merge()
        del self._ext_settings

    def _load_ext_settings(self,ext_settings):
        ext_settings = ext_settings or dict()

        if not isinstance(ext_settings,dict):
            ext_settings = import_module(ext_settings).__dict__
        self._ext_settings = ext_settings

    def _merge(self):
        for k,v in self._ext_settings.items():
            if k.startswith('_'):
                continue

            if isinstance(v,dict):
                self.settings[k].update(v)
            else:
                self.settings.update({k:v})

    def get(self,k,default = None):
        return self.settings.get(k,default)

    def update(self,k,v):
        self.settings.update(k,v)
