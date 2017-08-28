#coding=utf8
"""
@author: lshu
@file: __init__.py.py
@time: 2017/8/27 12:45
@desc: 
"""
import logging


logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
                # datefmt='%a, %d %b %Y %H:%M:%S',
                # filename='myapp.log',
                # filemode='w'
                    )

from .setting import SettingManager
from .collector import CollectorManager
from .verify import VerifyManager
from multiprocessing import Process

class Manager(object):
    def __init__(self,ext_settings = None):
        self.setting_manager = SettingManager(ext_settings or {})
        self.collector_manager = CollectorManager.from_setting_manager(self.setting_manager)
        self.verify_manager = VerifyManager.from_setting_manager(self.setting_manager)

    def run(self,join = True):
        ps = [
            Process(target=self.collector_manager.crawl, name='collector_manager'),
            Process(target=self.verify_manager.verify, name='verify_manager'),
        ]

        for p in ps:
            p.start()

        if join:
            for p in ps:
                p.join()
