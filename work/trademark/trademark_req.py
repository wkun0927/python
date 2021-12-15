# -*- coding: utf-8 -*-
# @Time : 2021/7/7-17:43
# @Author : Warren
# @Email : 18410065868@163.com
# @File : trademark_req.py
# @Project : pythonProject
# @Description : 使用requests请求

import requests


def get_proxies():
    ip_url = "http://152.136.208.143:5000/w/ip/random"
    proxies = requests.get(ip_url, headers={'User-Agent': 'Mozilla/5.0'}).json()
    return proxies


response = requests.post('http://sbj.cnipa.gov.cn/', verify=False)
print(response.content.decode('utf-8'))
