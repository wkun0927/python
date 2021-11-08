# -*- coding : utf-8 -*-
# @Time : 2021/6/30 9:27
# @Author : 王琨
# @Email : 18410065868@163.com
# @File : test_ip.py
# @Software : PyCharm
# @Description : 检查ip是否可用


import requests


def check_proxy(ip, port):
    """第二种："""
    try:
        proxy = 'http://{ip}:{port}'
        res = requests.get(url='http://icanhazip.com/', proxies={'http': proxy})
        proxyIP = res.text
        if proxyIP == proxy:
            print("代理IP:'" + proxyIP + "'有效！", proxy)
            return True
        else:
            print("2代理IP无效！", proxyIP, proxy)
            return False
    except:
        print("1代理IP无效！", proxyIP, proxy)
        return False


a = check_proxy('114.220.149.240', '57114')
print(a)
