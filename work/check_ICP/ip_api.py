# -*- coding: utf-8 -*-
# @Author            : 王琨
# @Email             : 18410065868@163.com
# @Date              : 2021-06-22 16:51:51
# @Last Modified by  : 王琨
# @Last Modified time: 2021-06-23 16:42:48
# @File Path         : D:\Dev\pythonProject\ip_api.py
# @Project Name      : pythonProject
# @Description       : IP代理

import time

import requests
from user_agent import generate_user_agent


def proxy():
    while True:
        url = 'http://17610040106.v4.dailiyun.com/query.txt?key=NP86444E99&word=&count=1&rand=false&ltime=0&norepeat=false&detail=false'
        headers = {
            "User-Agent": generate_user_agent()
        }
        response = requests.get(url, headers=headers)
        proxy_dly = response.text.strip()
        if proxy_dly:
            proxies = proxy_dly
            break
        else:
            time.sleep(15)
    return proxies


if __name__ == '__main__':
    a = proxy()
    print(a)
