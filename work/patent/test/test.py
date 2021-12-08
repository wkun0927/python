# -*- coding: utf-8 -*-
# @Author: wangkun
# @Date: 2021-12-07 10:43:03
# @Descripttion:

import requests


def get_proxies():
    ip_url = "http://192.168.10.25:8000/ip"
    proxies = requests.get(ip_url, headers={
        'User-Agent': 'Mozilla/5.0'
    }).json()
    print(proxies['http'])
    return proxies


cookies = {
    'WEE_SID': '7CABDDDC7DBBFA79535F49A157ACE3C8.pubsearch02',
    'IS_LOGIN': 'true',
    'JSESSIONID': '7CABDDDC7DBBFA79535F49A157ACE3C8.pubsearch02',
    'avoid_declare': 'declare_pass',
}

headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent':
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'http://60.166.52.165:8030',
    'Referer':
    'http://60.166.52.165:8030/pubsearch/patentsearch/tableSearch-showTableSearchIndex.shtml',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

data = {
    'searchCondition.searchExp':
    '\u7533\u8BF7\uFF08\u4E13\u5229\u6743\uFF09\u4EBA=(\u534E\u4E3A\u6280\u672F\u6709\u9650\u516C\u53F8)',
    'searchCondition.dbId': 'VDB',
    'searchCondition.searchType': 'Sino_foreign',
    'searchCondition.extendInfo[\'MODE\']': 'MODE_TABLE',
    'searchCondition.extendInfo[\'STRATEGY\']': 'STRATEGY_CALCULATE',
    'searchCondition.targetLanguage': '',
    'wee.bizlog.modulelevel': '0200201',
    'resultPagination.limit': '12'
}

response = requests.post(
    'http://60.166.52.165:8030/pubsearch/patentsearch/executeTableSearch-executeCommandSearch.shtml',
    headers=headers,
    cookies=cookies,
    data=data,
    # proxies=get_proxies(),
    verify=False)
print(response.status_code, response.text)
