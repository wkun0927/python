# -*- coding: utf-8 -*-
# @Author            : 王琨
# @Email             : 18410065868@163.com
# @Date              : 2021-06-21 09:41:11
# @Last Modified by  : 王琨
# @Last Modified time: 2021-06-29 14:42:29
# @File Path         : D:\Dev\pythonProject\软著查询.py
# @Project Name      : pythonProject
# @Description       : 中国版权保护中心

import time
import requests
from user_agent import generate_user_agent

from ip_api import proxy

value = input('请输入申请人：')
count = 1
Dict = {}
url = 'https://apis.imquzan.com/license/sCopyright'
headers = {
    'User-Agent': generate_user_agent()
}
proxy = proxy()
while True:
    try:
        params = (
            ('name', value),
            ('size', '10'),
            ('page', count),
            ('proxies', proxy),
        )
        response = requests.get(url=url, params=params, headers=headers)
        print(response.status_code)
        res = response.json()
        data = res.get('data').get('items')
        for item in data:
            Dict[item['fullname']] = item['regnum']
        print(Dict)
        count += 1
    except:
        break
