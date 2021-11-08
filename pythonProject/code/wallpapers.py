# -*- coding: utf-8 -*
# @Author: 王琨
# @Date: 2021-08-11 11:45:17
# @LastEditors: 王琨
# @LastEditTime: 2021-08-18 14:27:57
# @FilePath: /pythonProject/wallpapers.py
# @Description:

import requests
from requests.sessions import TooManyRedirects
from user_agent import generate_user_agent
from lxml import etree
import json
import csv
from requests.adapters import HTTPAdapter


def main():
    url_list = csv.reader(open('../data/page_url.csv', encoding='utf-8'))
    failed_url = []
    x = 1
    for url in url_list:
        headers = {'user-agent': generate_user_agent()}
        try:
            n_response = s.get(url[0], headers=headers)
            print(n_response.status_code)
            page_html = etree.HTML(n_response.text)
            max_page = page_html.xpath('//*[@id="next_button"]/span/text()[3]')
            max_page = max_page[0].split('/')[-1]
            max_num = int(max_page.split('\\')[0])
        except TooManyRedirects:
            failed_url.append(url)
            print(url)
            continue
        count = 1
        while count < max_num + 1:
            params = {('page', str(count))}
            response = s.get(url=url[0], headers=headers, params=params, timeout=10)
            html = etree.HTML(response.text)
            url_list = html.xpath('//*[@class="boxgrid"]/a/@href')
            for part in url_list:
                real_url = 'https://wall.alphacoders.com' + part
                List = [real_url]
                with open('../data/boxgrid_url.csv', 'a') as f:
                    f_csv = csv.writer(f)
                    f_csv.writerow(List)
            print(str(count))
            count += 1
        print('网址：{}'.format(x))
        x += 1


if __name__ == '__main__':
    s = requests.session()

    s.mount('http://', HTTPAdapter(max_retries=10))
    s.mount('https://', HTTPAdapter(max_retries=10))
    main()
