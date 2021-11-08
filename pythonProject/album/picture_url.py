# -*- coding: utf-8 -*
# @Author: 王琨
# @Date: 2021-08-18 14:22:18
# @LastEditors: 王琨
# @LastEditTime: 2021-08-18 14:35:47
# @FilePath: /pythonProject/album/picture_url.py
# @Description: 

import csv
import requests
from requests.adapters import HTTPAdapter
from user_agent import generate_user_agent
from lxml import etree
from multiprocessing import Process
import time


def main(a, b):
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=10))
    s.mount('https://', HTTPAdapter(max_retries=10))
    urls = []

    url_list = csv.reader(open('../data/boxgrid_url.csv', encoding='utf-8'))

    for url in url_list:
        urls.append(url[0])
    if b > len(urls):
        b = len(urls) + 1
    for x in range(a, b):
        headers = {
            'user-agent': generate_user_agent()
        }
        time.sleep(1)
        try:
            response = s.get(urls[x], headers=headers, timeout=30)
            html = etree.HTML(response.text)
            picture_url = html.xpath('//*[@class="center img-container-desktop"]/a/@href')
            print(str(x))
            with open('../data/picture_url.csv', 'a') as f:
                f_csv = csv.writer(f)
                f_csv.writerow(picture_url)
        except :
            headers = {
                'user-agent': generate_user_agent()
            }
            continue


if __name__ == '__main__':
    process_list = []
    for i in range(20):
        p = Process(target=main, args=(i*16500, (i+1)*16500))
        p.start()
        process_list.append(p)

    for p in process_list:
        p.join()

    print('运行结束')
