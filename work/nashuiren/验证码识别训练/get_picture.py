#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-09-01 14:50:22
# @LastEditors: 王琨
# @LastEditTime: 2021-09-01 14:50:22
# @FilePath: /python/工作内容/一般纳税人/验证码识别训练/get_picture.py
# @Description: image下载

import requests
from user_agent import generate_user_agent


for i in range(1, 1001):
    headers = {
        'User-Agent': generate_user_agent(),
    }
    response = requests.get('https://etax.fujian.chinatax.gov.cn/tycx-cjpt-web/cxptGz/builderCaptcha.do', headers=headers)

    with open('/home/wk/Dev/image/' + str(i) + '.png', 'wb') as f:
        f.write(response.content)
