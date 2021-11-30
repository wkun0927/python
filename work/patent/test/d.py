#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-11-10 09:32:16
# @Descripttion: 拆分字典

import json

import redis
import requests

req = requests.get('http://mail.ewomail.cn:8000')
print(req.text)
