#!user/bin/env python
# @# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-08-09 20:39:37
# @LastEditors: 王琨
# @LastEditTime: 2021-08-19 12:01:58
# @FilePath: /pythonProject/时间格式转换.py
# @Description: 时间戳转换

import time

timestamp = 1630048153
dateArray = time.localtime(timestamp)
otherStyleTime = time.strftime('%Y-%m-%d %H:%M:%S', dateArray)

print(int(time.time()) * 1000)
