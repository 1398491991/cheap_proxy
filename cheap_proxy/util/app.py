#!/usr/bin/env python
#coding=utf-8

"""
@author: lshu
@file: api.py
@time: 2017-08-29 16:38
@desc: 
"""
from flask import Flask
import logging

logger = logging.getLogger(__name__)
app = Flask(__name__)

@app.route('/')
def index():
    return u'test'