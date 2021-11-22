#! user/bin/env python
# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-08-23 16:14:06
# @LastEditors: 王琨
# @LastEditTime: 2021-08-25 11:29:23
# @FilePath: /python/工作内容/税务/qinghai.py
# @Description: 

import requests
from user_agent import generate_user_agent
from lxml import etree
import csv


headers = {
    'user-agent': generate_user_agent()
}
url = 'http://qinghai.chinatax.gov.cn/web/zdsswfsxaj/zdaj.shtml'

response = requests.get(url=url, headers=headers, verify=False)
html = etree.HTML(response.text)

# 获取每一个城市的网址
city_url = []
count = 1
while True:
    part_url = html.xpath('//*[@id="slider2"]/dt[' + str(count) + ']/a/@href')
    if part_url:
        url = 'http://qinghai.chinatax.gov.cn' + part_url[0]
        city_url.append(url)
        count += 1
    else:
        break

# 获取详细数据页面网址
info_url_list = []
for url in city_url:
    k = 1
    while True:
        if k == 1:
            city_url = url
        else:
            city_url = url.replace('iframe', 'iframe_' + str(k))
        k += 1
        info_res = requests.get(url=city_url, headers=headers, verify=False)
        if info_res.status_code == 404:
            break
        else:
            html = etree.HTML(info_res.text)
            for x in range(1, 11):
                part_info_url = html.xpath('//ul[' + str(x) + ']/li/a/@href')
                if not part_info_url:
                    continue
                info_url = 'http://qinghai.chinatax.gov.cn' + part_info_url[0]
                info_url_list.append(info_url)

# 获取详情页的数据
for info_url in info_url_list:
    item_res = requests.get(url=info_url, headers=headers, verify=False)
    html = etree.HTML(item_res.text)
    for i in range(1, 20):
        info = html.xpath('//*[@id="main"]//tbody/tr[' + str(i) + ']//span//text()')
        if not info:
            continue
        with open('./data/qinghai.csv', 'a') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(info)
