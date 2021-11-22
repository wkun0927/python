# -*- coding: utf-8 -*-
# @Author: 王琨
# @Email: 18410065868@163.com
# @Date: 2021-06-15 09:31:34
# @Description:

import csv

import requests
from fake_useragent import UserAgent
from lxml import etree

ua = UserAgent()
agent = ua.random
headers = {
    'User-Agent': agent
}

with open('gs_url.csv', 'r', encoding='utf-8') as f:
    gs_dict = dict(csv.reader(f))

with open('gg_url.csv', 'r', encoding='utf-8') as s:
    gg_dict = dict(csv.reader(s))

gs_file_url_list = {}
gg_file_url_list = {}

# 公示文件获取(gg)
for key in gs_dict:
    gs_url = gs_dict[key]
    # print(gs_url)
    response = requests.get(url=gs_url, headers=headers)
    # print(response.content.decode('utf-8'))
    # break
    html = etree.HTML(response.content.decode('utf-8'))
    gs_href = html.xpath('//*[@id="detailContent"]//a/@href')
    gs_file_url = ('/'.join(gs_url.split('/')[:-1])) + '/' + gs_href[0]
    # print(gs_file_url)
    req = requests.get(url=gs_file_url, headers=headers, stream=True)
    name = key
    with open('D:/Dev/gs_file/' + name + '.pdf', 'wb') as f:
        f.write(req.content)

for key in gg_dict:
    gg_url = gg_dict[key]
    # print(gg_url)
    response = requests.get(url=gg_url, headers=headers)
    # print(response.content.decode('utf-8'))
    # break
    html = etree.HTML(response.content.decode('utf-8'))
    gg_href = html.xpath('//*[@id="detailContent"]//a/@href')
    gg_file_url = ('/'.join(gg_url.split('/')[:-1])) + '/' + gg_href[0]
    # print(gs_file_url)
    req = requests.get(url=gg_file_url, headers=headers, stream=True)
    name = key
    with open('D:/Dev/gg_file/' + name + '.pdf', 'wb') as f:
        f.write(req.content)
