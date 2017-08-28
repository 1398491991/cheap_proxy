#coding=utf8
"""
@author: lshu
@file: __init__.py.py
@time: 2017/8/27 12:43
@desc: 
"""

class a(object):
    def __iter__(self):
        yield 1

    def __next__(self):
        yield 2


print(iter(a))
print(iter(a))
print(iter(a))
print(iter(a))
