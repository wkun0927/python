#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-07-29 17:15:42
# @LastEditors: 王琨
# @LastEditTime: 2021-08-03 15:41:49
# @FilePath: \pythonProject\picture.py
# @Descripttion:

import json
import requests
from requests.adapters import HTTPAdapter
import time
from user_agent import generate_user_agent
import csv
from multiprocessing import Process


def main(num):
    headers = {'User-Agent': generate_user_agent()}
    while num < 180259:
        try:
            time.sleep(1)
            response = s.get(url=url_list[num], headers=headers, timeout=15)
            picture_name = url_list[num].split('.')[-1]
            with open('/home/kerwin/Dev/album/' + str(num) + '.' + picture_name, 'wb') as pic:
                pic.write(response.content)
            print(str(num))
            num += 1
        except:
            headers = {'User-Agent': generate_user_agent()}
            print('***' * 20)
            continue


if __name__ == '__main__':
    s = requests.Session()

    s.mount('http://', HTTPAdapter(max_retries=10))
    s.mount('https://', HTTPAdapter(max_retries=10))

    with open('../data/gamewallpaper.json') as f:
        url_list = json.loads(f.read())

    main(90)
