#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-11-10 09:32:16
# @Descripttion: 拆分字典

import json

import redis
import requests


def get_proxies():
    ip_url = "http://192.168.10.25:5000/w/ip/random"
    proxies = requests.get(ip_url, headers={'User-Agent': 'Mozilla/5.0'}).json()
    return proxies

a = get_proxies()
print(a)
