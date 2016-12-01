# -*- coding:utf-8 -*-
"""
@author: yangmqglobe
@file: saveimages.py
@time: 2016/11/29
"""
from bs4 import BeautifulSoup
from functools import wraps
from .spidry import response
import requests
import time


class saveimages:
    """
    修饰器类
    """

    def __init__(self,
                 feature='html',
                 method='get',
                 sleep=0,
                 log=True,
                 **kwargs):
        """
        构造方法，初始化各种参数
        :param feature: 解析请求数据的方法，暂时分为html的soup和json
        :param method: 请求页面的方法
        :param sleep: 保存图片时每张图片的请求时间间隔
        :param log: 是否打印log
        :param kwargs: 其他的关键词参数，与requests库的参数相关
        """
        self.feature = feature
        self.method = method
        self.sleep = sleep
        self.log = log
        self.kwargs = kwargs

    def __call__(self, fn):
        """
        类被作为修饰器调用时调用方法
        :param fn:
        :return:
        """

        @wraps(fn)
        def wrapper(url, method='get', **kwargs):
            """
            修饰后的方法的实现
            :param url: 需要请求的页面地址
            :param method: 请求的方法
            :param kwargs: 其他请求参数
            """
            self._fetchpage(url, method, **kwargs)
            imglist = fn()  # 调用原始方法，获得图片列表
            for img in imglist:  # 循环保存图片
                self.saveimage(img)

        return wrapper

    def _fetchpage(self, url, method, **kwargs):
        """
        请求页面并解析为相应的解析对象
        :param url:请求页面的url
        :param method:请求方法
        :param kwargs:其他请求尝试
        """
        if self.log:
            print('fetch:' + url)
        response.r = requests.request(method, url, **kwargs)
        response.text = response.r.text
        if self.feature.lower() == 'html':  # 将结果解析为soup
            response.soup = BeautifulSoup(response.text, 'lxml')
            response.json = None
        elif self.feature.lower() == 'json':  # 将结果解析为json
            response.json = response.r.json()
            response.soup = None

    def saveimage(self, img):
        """
        保存图片函数
        :param img: 包含图片url和保存路径的字典
        :return:
        """
        url = img['url']
        path = img['path']
        r = requests.request(self.method, url, **self.kwargs)
        with open(path, 'wb') as img:
            img.write(r.content)
        if self.log:
            print('save:' + path)
        time.sleep(self.sleep)
