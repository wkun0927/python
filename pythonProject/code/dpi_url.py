# -*- coding: utf-8 -*
# @Author: 王琨
# @Date: 2021-08-13 16:23:19
# @LastEditors: 王琨
# @LastEditTime: 2021-08-18 14:38:23
# @FilePath: /pythonProject/dpi_url.py
# @Description:

import requests
from lxml import etree
import csv
from user_agent import generate_user_agent
from requests.adapters import HTTPAdapter

s = requests.session()

s.mount('http://', HTTPAdapter(max_retries=10))
s.mount('https://', HTTPAdapter(max_retries=10))
s.keep_alive = False
url_list = csv.reader(open('./data/dpi.csv', encoding='utf-8'))
num = 40
for url in url_list:
    try:
        picture_url = csv.reader(open('./data/' + str(num) + '.csv', encoding='utf-8'))
        picture_url_list = []
        for i in picture_url:
            picture_url_list.append(i)
    except :
        picture_url_list = []
    headers = {'user-agent': generate_user_agent()}
    n_response = s.get(url[0], headers=headers)
    print(n_response.status_code)
    page_html = etree.HTML(n_response.text)
    max_page = page_html.xpath('//*[@id="next_button"]/span/text()[3]')
    max_page = max_page[0].split('/')[-1]
    max_num = int(max_page.split('\\')[0])
    count = 1
    while count < max_num + 1:
        params = {('page', str(count))}
        response = s.get(url=url[0],
                         headers=headers,
                         params=params,
                         timeout=60, verify=False)
        html = etree.HTML(response.text)
        url_list = html.xpath('//*[@class="boxgrid"]/a/@href')
        for part in url_list:
            real_url = 'https://wall.alphacoders.com' + part
            if real_url not in picture_url_list:
                picture_url_list.append(real_url)
                List = []
                List.append(real_url)
                with open('./data/' + str(num) + '.csv', 'a') as f:
                    f_csv = csv.writer(f)
                    f_csv.writerow(List)
            else:
                break
        print(str(count))
        count += 1
    print('网址：{}'.format(num))
    num += 1
