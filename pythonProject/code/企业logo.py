# -*- coding: utf-8 -*-
# @Author            : 王琨
# @Email             : 18410065868@163.com
# @Date              : 2021-06-18 16:44:38
# @Last Modified by  : 王琨
# @Last Modified time: 2021-06-23 16:45:40
# @File Path         : D:\Dev\pythonProject\企业logo.py
# @Project Name      : pythonProject
# @Description       : 

import time
from urllib.parse import quote

import requests
from lxml import etree
from user_agent import generate_user_agent

start = time.time()
xpath = '//div[@class="summary-pic"]/a/@href'
company = quote(input('请输入公司名称：'))
url = 'https://baike.baidu.com/item/' + company
headers = {
    'User-Agent': generate_user_agent()
}

response = requests.get(url, headers=headers)
html = etree.HTML(response.content)
logo_url = 'https://baike.baidu.com/pic/' + company + html.xpath(xpath)[0]
print(logo_url)
end = time.time()
print(end - start)
