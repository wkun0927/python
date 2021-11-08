# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date:   2021-05-27 13:52:15
# @Last Modified by:   王琨
# @Last Modified time: 2021-06-16 17:45:28
import json
from http import cookiejar
from urllib import request

from lxml import etree

cookie = cookiejar.CookieJar()
cookie_handle = request.HTTPCookieProcessor(cookie)
http_handle = request.HTTPHandler()
https_handle = request.HTTPSHandler()
opener = request.build_opener(cookie_handle, http_handle, https_handle)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3870.400 QQBrowser/10.8.4405.400'
}
with open('comUrl.json', 'r') as f:
    Dict = json.loads(f.read().encode('utf-8'))
for Name in Dict:
    Url = Dict[Name]
    if Url != '没有官网':
        response = request.Request(Url, headers=headers)
        html = opener.open(response).read().decode()
        html = etree.HTML(html)
        Infos = html.xpath('//*[contains(@class,"logo")]//img[@src]')
        for item in range(len(Infos)):
            Info = Infos[item]
            print(Name, Info)

# xpath = '//*[contains(@class,"logo")]//img'
# //*[@id="key"]