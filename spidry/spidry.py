# -*- coding:utf-8 -*-
"""
@author: yangmqglobe
@file: spidry.py
@time: 2016/11/29
"""
from threading import local
from requests.models import Response
from bs4 import BeautifulSoup


class Spidry(local):
    def __init__(self):
        self.soup = BeautifulSoup(features='lxml')
        self.json = {}
        self.r = Response()
        self.text = ''


response = Spidry()
