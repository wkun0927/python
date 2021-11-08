# -*- coding: utf-8 -*
# @Author: 王琨
# @Date: 2021-08-09 20:39:37
# @LastEditors: 王琨
# @LastEditTime: 2021-08-11 16:36:57
# @FilePath: /pythonProject/konachan.py
# @Description: 

# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-07-30 13:44:33
# @LastEditors: 王琨
# @LastEditTime: 2021-08-04 08:51:01
# @FilePath: \pythonProject\konachan.py
# @Descripttion:

import requests
from requests.adapters import HTTPAdapter
from user_agent import generate_user_agent
from lxml import etree
import json
import time
from random import randint
from multiprocessing import Process


def main(i, count):
    s = requests.session()

    s.mount('http://', HTTPAdapter(max_retries=10))
    s.mount('https://', HTTPAdapter(max_retries=10))

    picture_url_list = []
    headers = {'User-Agent': generate_user_agent()}

    URL = 'https://konachan.net/post'

    while i < count:
        try:
            params = (
                ('page', str(i)),
                ('tags', ''),
            )
            response = s.get(URL, headers=headers, params=params, timeout=10)
            html = etree.HTML(response.text)
            url_largeimg = html.xpath('//*[@class="directlink largeimg"]/@href')
            url_smallimg = html.xpath('//*[@class="directlink smallimg"]/@href')
            for url in url_largeimg:
                picture_url_list.append(url)
            for url in url_smallimg:
                picture_url_list.append(url)
            print(str(i))
            i += 1
        except:
            print('***' * 20)
            continue

    with open('gamewallpaper.json', 'a') as f:
        json.dump(picture_url_list, f)


if __name__ == '__main__':
    process_list = []
    for i in range(10):
        p = Process(target=main, args=(i * 1250 + 1, (i + 1) * 1250 + 1))
        p.start()
        process_list.append(p)
    for p in process_list:
        p.join()
