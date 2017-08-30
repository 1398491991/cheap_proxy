#!/usr/bin/env python
#coding=utf-8

"""
@author: lshu
@file: test.py
@time: 2017-08-28 10:53
@desc: 
"""
# from gevent import monkey
# monkey.patch_socket()
from cheap_proxy.manager import Manager
test = Manager()
test.setup_blocking_scheduler()
test.add_default_service()
test.start()
