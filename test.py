# -*- coding:utf-8 -*-
"""
@author: yangmqglobe
@file: test.py
@time: 2016/11/28
"""
from spidry import saveimages
from spidry import response as resp
import os


@saveimages(feature='json', sleep=3)# 使用修饰器修饰解析方法
def bilibili():
    # 解析方法，生成包含需要保存图片url和路径的字典列表
    iconlist = [{'url': icon['icon'],
                 'path': 'icon/'+icon['title']+'.gif'}
                for icon in resp.json['fix']]
    return iconlist


if __name__ == '__main__':
    if not os.path.exists("icon"):
        os.makedirs("icon")
    # 调用被修饰的方法！
    bilibili("http://www.bilibili.com/index/index-icon.json")
    print("done!")
