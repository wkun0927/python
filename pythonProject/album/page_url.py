# -*- coding: utf-8 -*
# @Author: 王琨
# @Date: 2021-08-18 15:03:09
# @LastEditors: 王琨
# @LastEditTime: 2021-08-18 15:03:20
# @FilePath: /pythonProject/album/page_url.py
# @Description: 

import requests
import csv
from lxml import etree
from user_agent import generate_user_agent

url = 'https://wall.alphacoders.com/#more_nav'
headers = {
    'user-agent': generate_user_agent()
}
response = requests.get(url, headers)
html = etree.HTML(response.text)
urls = html.xpath('//*[@id="categories"]/a/@href')
for url in urls:
    real_url = 'https://wall.alphacoders.com/' + url
    List = []
    List.append(real_url)
    with open('../data/page_url.csv', 'a') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(List)