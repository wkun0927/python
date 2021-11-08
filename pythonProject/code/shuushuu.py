# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-07-29 14:55:12
# @LastEditors: 王琨
# @LastEditTime: 2021-07-29 17:14:49
# @FilePath: \pythonProject\shuushuu.py
# @Descripttion: shuu网站图片链接

import requests
from lxml import etree
from user_agent import generate_user_agent
import json
import time


def get_proxies():
    ip_url = "http://152.136.208.143:5000/w/ip/random"
    proxies = requests.get(ip_url, headers={'User-Agent': 'Mozilla/5.0'}).json()
    print(proxies['https'])
    return proxies['https']


def main():
    start_time = time.time()
    url_list = []
    try:
        url = 'https://e-shuushuu.net/?page=1'
        headers = {
            'User-Agent': generate_user_agent()
        }
        proxies = {
            'http:': get_proxies()
        }
        response = requests.get(url=url, headers=headers, proxies=proxies)
        html = etree.HTML(response.text)
        shuu_url_list = html.xpath('//a[@class="thumb_image"]/@href')
        for url in shuu_url_list:
            shuu_url = 'https://e-shuushuu.net/' + url
            url_list.append(shuu_url)
    except Exception as e:
        print(e)

    with open('shuu_url.json', 'w') as f:
        json.dump(url_list, f)
        begin_time = time.time()
        print(begin_time - start_time)


if __name__ == '__main__':
    main()