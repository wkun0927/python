#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-11-10 09:32:16
# @Descripttion: 拆分字典

import redis
import requests


def get_proxies():
    ip_url = "http://192.168.10.25:8000/ip"
    proxies = requests.get(ip_url, headers={
        'User-Agent': 'Mozilla/5.0'
    }).json()
    print(proxies)
    proxy = 'http://' + proxies['http'].split('@')[-1]
    print(proxy)
    return proxy


get_proxies()
