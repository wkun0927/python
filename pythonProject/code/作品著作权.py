# -*- coding: utf-8 -*-
# @Author            : 王琨
# @Email             : 18410065868@163.com
# @Date              : 2021-06-16 20:35:58
# @Last Modified by  : 王琨
# @Last Modified time: 2021-06-29 15:53:20
# @File Path         : D:\Dev\pythonProject\作品著作权.py
# @Project Name      : pythonProject
# @Description       : 暂时只能用版权保护中心获取(requests)

import time
from user_agent import generate_user_agent
import requests
import urllib
from urllib import request
import ipdb


url = 'http://www.ccopyright.com.cn/'
headers = {
    'User-Agent': generate_user_agent()
}


def proxy():
    while True:
        ip_api = 'http://17610040106.v4.dailiyun.com/query.txt?key=NP86444E99&word=&count=1&rand=false&ltime=0&norepeat=false&detail=false'
        res = requests.get(ip_api, headers=headers)
        proxy_dly = res.text.strip()
        if proxy_dly:
            break
        else:
            pass
    return proxy_dly


