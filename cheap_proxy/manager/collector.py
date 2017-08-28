#coding=utf8
"""
@author: lshu
@file: collector.py
@time: 2017/8/27 12:47
@desc: 
"""


from ..util.misc import import_module_from_str


class CollectorManager(object):



    def __init__(self,setting_manager):
        self.setting_manager = setting_manager

    @classmethod
    def from_setting_manager(cls,setting_manager):
        return cls(setting_manager)


    def make_raw_proxy_queue(self):
        raw_queue_class_path = self.setting_manager.get('RAW_QUEUE_CLASS','cheap_proxy.queue.redis_queue.RedisQueue')
        raw_queue_key = self.setting_manager.get('RAW_QUEUE_KEY','cheap_proxy:raw_proxy')
        raw_db_class_path = self.setting_manager.get('RAW_DB_CLASS', 'cheap_proxy.db.redis_db.RedisDb')

        server = import_module_from_str(raw_db_class_path).from_setting_manager(self.setting_manager)
        self._raw_proxy_queue = import_module_from_str(raw_queue_class_path)(server,raw_queue_key)

    @property
    def raw_proxy_queue(self):
        return self._raw_proxy_queue


    def load_collector(self):
        # 加载各个采集类
        self.collectors = []
        collectors_map = self.setting_manager.get('COLLECTORS',{})
        for k,v in collectors_map.items():
            if v:
                collector = import_module_from_str(k).from_setting_manager(self.setting_manager)
                self.collectors.append(collector)

    def get_collector_parallel_size(self):
        # 计算合适的处理池大小
        collectors_len = len(self.collectors)
        collector_parallel_size = self.setting_manager.get('COLLECTOR_PARALLEL_SIZE',collectors_len)
        if collector_parallel_size > collectors_len:
            collector_parallel_size = collectors_len

        return collector_parallel_size

    def make_parallel_pool(self):
        size = self.get_collector_parallel_size()
        collector_pool_class_path = self.setting_manager.get('COLLECTOR_POOL_CLASS','gevent.pool.Pool')
        if 'gevent' in collector_pool_class_path:
            from gevent import monkey
            monkey.patch_socket()

        return import_module_from_str(collector_pool_class_path)(size)

    def crawl(self):
        # 并行运行采集类
        self.load_collector()
        self.make_raw_proxy_queue()
        self.collector_pool = self.make_parallel_pool()
        self.collector_pool.map(self._run_collector_crawl,self.collectors)


    def _run_collector_crawl(self,collector):
        # 迭代采集器采集的代理
        for safe_proxy in collector.crawl():
            if safe_proxy:
                self.raw_proxy_queue.push(safe_proxy.serialize())

