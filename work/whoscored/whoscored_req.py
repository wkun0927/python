# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-12-09 18:29:35
# @Descripttion:

import random

import requests
from fake_useragent import UserAgent


def get_proxies():
    ip_url = "http://192.168.10.25:8000/ip"
    proxies = requests.get(ip_url, headers={'User-Agent': 'Mozilla/5.0'}).json()
    print(proxies)
    return proxies


def main():
    ua = UserAgent()
    user_anget = ua.random
    url = 'https://www.whoscored.com/'
    headers = {"User-Agent": user_anget}
    print(user_anget)
    res = requests.get(url=url, headers=headers, proxies=get_proxies(), verify=False)
    print(res.text)


if __name__ == "__main__":
    main()
