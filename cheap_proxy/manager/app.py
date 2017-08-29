#!/usr/bin/env python
#coding=utf-8

"""
@author: lshu
@file: app.py
@time: 2017-08-29 16:56
@desc: 
"""
import pprint
import logging
from ..util.misc import import_module_from_str

logger = logging.getLogger(__name__)

class AppManager(object):

    def __init__(self,setting_manager):
        self.setting_manager = setting_manager
        self.setup_app()


    @classmethod
    def from_setting_manager(cls,setting_manager):
        return cls(setting_manager)


    def setup_app(self):
        self.app = import_module_from_str(self.setting_manager['APP'])
        self.app_run_config = self.setting_manager['APP_RUN_CONFIG']
        logger.info('APP_RUN_CONFIG :\n%s'%pprint.pformat(self.app_run_config))

    def run(self):
        self.app.run(**self.app_run_config)
