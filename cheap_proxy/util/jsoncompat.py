#!/usr/bin/env python
#coding=utf-8

"""
@author: lshu
@file: jsoncompat.py
@time: 2017-08-28 16:41
@desc: 
"""
import json

def loads(s):
    return json.loads(s)



def dumps(obj):
    return json.dumps(obj)
