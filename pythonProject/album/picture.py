#! user/bin/env python
# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-08-19 16:12:33
# @LastEditors: 王琨
# @LastEditTime: 2021-08-19 16:13:47
# @FilePath: /pythonProject/album/picture.py
# @Description: 获取图片

import requests
from requests.adapters import HTTPAdapter
from lxml import etree
from user_agent import generate_user_agent
from multiprocessing import Process
import csv


def main():
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=10))
    s.mount('https://', HTTPAdapter(max_retries=10))

    urls = []

    url_list = csv.reader(open('../data/picture_url.csv', encoding='utf-8'))
    x = 0
    for url in url_list:
        urls.append(url)
        headers = {
            'user-agent': generate_user_agent()
        }
        response = s.get(url[0], headers=headers)
        pic_type = url[0].split('.')[-1]
        with open('/home/kerwin/Dev/python/albums/' + str(x + 1) + '.' + pic_type, 'wb') as f:
            f.write(response.content)
        print(x)
        x += 1


if __name__ == '__main__':
    main()
