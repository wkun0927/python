#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-11-10 09:32:16
# @Descripttion: 拆分字典

import json

with open('./data/总网站.json') as f:
    userinfo = json.load(f)
num = 1
count = 1
cookie = dict()
for username in userinfo.keys():
    if num > 20:
        cookie.clear()
        count += 1
        num = 1
    cookie[username] = userinfo[username]
    num += 1
    with open('./data/userinfo' + str(count) + '.json', 'w') as s:
        json.dump(cookie, s)
