#coding=utf8
"""
@author: lshu
@file: collector.py
@time: 2017/8/27 12:47
@desc: 
"""


from .crawl import CrawlManager
import logging
import pprint
from ..util.misc import import_module_from_str

logger = logging.getLogger(__name__)


class CollectorManager(CrawlManager):


    def setup_collector(self):
        # 加载各个采集类
        self._collectors = []
        collectors_map = self.setting_manager['COLLECTORS']
        logger.info('COLLECTORS :\n%s'%pprint.pformat(collectors_map))
        for k,v in collectors_map.items():
            if v:
                collector = import_module_from_str(k).from_setting_manager(self.setting_manager)
                self._collectors.append(collector)
                logger.info('setup collector :%s'%k)

    @property
    def collectors(self):
        if not hasattr(self,'_collectors'):
            self.setup_collector()

        return self._collectors


    def get_parallel_size(self):
        # 计算合适的处理池大小
        collectors_len = len(self.collectors)
        size = self.setting_manager['COLLECTOR_PARALLEL_SIZE']
        if size > collectors_len:
            size = collectors_len
        logger.info('COLLECTOR_PARALLEL_SIZE :%s' % size)
        return size



    def run(self):
        # 运行所有采集器
        logger.debug('run collector')
        self.collector_pool.map(self.map_run, self.collectors)

    def map_run(self,collector):
        # 迭代采集器采集的代理
        for safe_proxy in collector.crawl():
            if safe_proxy:
                logger.debug('push new safe_proxy :%s'%safe_proxy)
                self.raw_proxy_queue.push(safe_proxy.to_base_dict())
