# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-08-09 20:39:37
# @Description: 高新技术企业认定管理工作网

import csv
import random
import time
from datetime import datetime

import requests
from user_agent import generate_user_agent
from lxml import etree

url_dict_gs = {}
url_dict_gg = {}
url_dict_file_gs = {}
url_dict_file_gg = {}

# 进入高新技术企业认定工作网
first_url = 'http://www.innocom.gov.cn/'
headers = {
    'User-Agent': generate_user_agent()
}

response = requests.get(url=first_url, headers=headers)
html = etree.HTML(response.text.encode('utf-8'))

# 拿到各地工信企业认定名单的网址（公示）
href_list_gs = html.xpath('//div[@class="content"][1]/a/@href')

for item in href_list_gs:
    url_dict_gs['http://www.innocom.gov.cn' + '/'.join(item.split('/')[:-1])] = item.split('/')[-1]

# 公告
href_list_gg = html.xpath('//div[@class="content"][2]/a/@href')

for item in href_list_gg:
    url_dict_gg['http://www.innocom.gov.cn' + '/'.join(item.split('/')[:-1])] = item.split('/')[-1]
# print(url_dict_gs, url_dict_gg)

# 遍历URL列表，获取文件地址
for url in url_dict_gs:
    time.sleep(random.randint(1, 5))
    city_page = requests.get(url=url + '/' + url_dict_gs[url], headers=headers)
    city_page_html = etree.HTML(city_page.content.decode('utf-8'))
    while True:
        for num in range(3):  # 获取三年内的通知文件的链接
            Year = str(datetime.now().year - num - 1)
            co_urls = city_page_html.xpath('//ul[@class="list"]//a[contains(text(),'
                                           + Year + ')]/@href')
            Name = city_page_html.xpath('//ul[@class="list"]//a[contains(text(),'
                                        + Year + ')]/text()')
            count = 0
            for part_url in co_urls:
                name = Name[count]
                co_list_url = 'http://www.innocom.gov.cn' + part_url
                url_dict_file_gs[name] = co_list_url
                count += 1
        try:
            next_page_url = city_page_html.xpath('//span[@class="arrow"]/a[contains(text(), " > ")]/@href')
        except Exception as e:
            print('公示：{}'.format(e))
            break
        next_page = requests.get(url='url' + next_page_url, headers=headers)
        city_page_html = etree.HTML(next_page.content.decode('utf-8'))

for url in url_dict_gg:
    time.sleep(random.randint(1, 4))
    city_page = requests.get(url=url + '/' + url_dict_gg[url], headers=headers)
    city_page_html = etree.HTML(city_page.content.decode('utf-8'))
    while True:
        co_urls = city_page_html.xpath('//ul[@class="list"]/li/a/@href')
        Name = city_page_html.xpath('//ul[@class="list"]/li/a/text()')
        count = 0
        for part_url in co_urls:
            name = Name[count]
            co_list_url = 'http://www.innocom.gov.cn' + part_url
            url_dict_file_gg[name] = co_list_url
            count += 1
        try:
            next_page_url = city_page_html.xpath('//span[@class="arrow"]/a[contains(text(), " > ")]/@href')
        except Exception as e:
            print('公告{}'.format(e))
            break
        next_page = requests.get(url='url' + next_page_url, headers=headers)
        city_page_html = etree.HTML(next_page.content.decode('utf-8'))
# print(url_dict_file_gs, url_dict_file_gg)

with open('./gs_url.csv', 'w', newline='', encoding='utf-8') as f:
    f_csv = csv.writer(f)
    for name in url_dict_file_gs:
        f_csv.writerow([name, url_dict_file_gs[name]])

with open('./gg_url.csv', 'w', newline='', encoding='utf-8')as s:
    s_csv = csv.writer(s)
    for name in url_dict_file_gg:
        s_csv.writerow([name, url_dict_file_gg[name]])
