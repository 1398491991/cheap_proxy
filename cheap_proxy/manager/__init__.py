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
                # filename='cheap_proxy.log',
                # filemode='w'
                    )

from .setting import SettingManager
from .collector import CollectorManager
from .verify import VerifyManager
from .store import StoreManager
from .app import AppManager
from multiprocessing import Process
from apscheduler.schedulers.blocking import BlockingScheduler


logger = logging.getLogger(__name__)

class Manager(object):
    def __init__(self,ext_settings = None):
        self.setting_manager = SettingManager(ext_settings or {})

    def setup_blocking_scheduler(self):
        blocking_scheduler_config = self.setting_manager['BLOCKING_SCHEDULER_CONFIG']
        self.blocking_scheduler = BlockingScheduler(**blocking_scheduler_config)

    def add_crontab_job(self,*args,**kwargs):
        # 提供添加定时任务的接口
        return self.blocking_scheduler.add_job(*args,**kwargs)

    def add_collector_service(self,trigger = 'interval', minutes=10,**kwargs):
        self.collector_manager = CollectorManager.from_setting_manager(self.setting_manager)
        self.add_crontab_job(self.collector_manager.run,
                             trigger = trigger,
                             minutes = minutes,
                             **kwargs)

    def add_verify_service(self,trigger = 'interval', minutes=10,**kwargs):
        self.verify_manager = VerifyManager.from_setting_manager(self.setting_manager)
        self.add_crontab_job(self.verify_manager.run,
                             trigger = trigger,
                             minutes = minutes,
                             **kwargs)

    def add_store_service(self,trigger = 'interval', minutes=10,**kwargs):
        self.store_manager = StoreManager.from_setting_manager(self.setting_manager)
        self.add_crontab_job(self.store_manager.run,
                             trigger = trigger,
                             minutes = minutes,
                             **kwargs)


    def add_app_service(self):
        # 添加 web 服务 ，非定时任务
        self.app_manager = AppManager.from_setting_manager(self.setting_manager)


    def add_default_service(self):
        # 启用默认服务 ，快捷方式
        self.add_collector_service()
        self.add_verify_service()
        self.add_store_service()
        self.add_app_service()


    def run_app_service(self):
        # 提供启动 web 服务的快捷方式 ，创建新进程
        p = Process(target=self.app_manager.run,name='app_process')
        p.start()
        logger.info('app_process pid<%s>'%p.pid)


    def start(self,daemon = False):
        # 守护暂未实现
        logger.info('all service is running...')
        self.run_app_service()
        self.blocking_scheduler.start()



    run = start
