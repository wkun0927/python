#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-11-12 10:13:57
# @Descripttion: 检查cookie是否有效

import csv
import json
import time

import requests


def get_proxies():
    ip_url = "http://152.136.208.143:5000/w/ip/random"
    proxies = requests.get(ip_url, headers={'User-Agent': 'Mozilla/5.0'}).json()
    print(proxies['http'])
    return proxies


def main():
    with open('./data/cookie.json') as f:
        cookie = json.load(f)

    index = []
    proxies = get_proxies()
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'http://123.233.113.66:8060',
        'Referer': 'http://123.233.113.66:8060/pubsearch/patentsearch/tableSearch-showTableSearchIndex.shtml',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    }

    data = {
        'resultPagination.limit': '12',
        'resultPagination.sumLimit': '10',
        'resultPagination.start': '12',
        'resultPagination.totalCount': '170000',
        'searchCondition.sortFields': '-APD,+PD',
        'searchCondition.searchType': 'Sino_foreign',
        'searchCondition.originalLanguage': '',
        'searchCondition.extendInfo[\'MODE\']': 'MODE_TABLE',
        'searchCondition.extendInfo[\'STRATEGY\']': 'STRATEGY_CALCULATE',
        'searchCondition.searchExp': '\u7533\u8BF7\uFF08\u4E13\u5229\u6743\uFF09\u4EBA=(\u534E\u4E3A\u6280\u672F\u6709\u9650\u516C\u53F8)',
        'searchCondition.executableSearchExp': 'VDB:(PAVIEW=\'\u534E\u4E3A\u6280\u672F\u6709\u9650\u516C\u53F8\')',
        'searchCondition.dbId': '',
        'searchCondition.literatureSF': '\u7533\u8BF7\uFF08\u4E13\u5229\u6743\uFF09\u4EBA=(\u534E\u4E3A\u6280\u672F\u6709\u9650\u516C\u53F8)',
        'searchCondition.targetLanguage': '',
        'searchCondition.resultMode': 'undefined',
        'searchCondition.strategy': '',
        'searchCondition.searchKeywords': '[\u534E][\u4E3A][\u6280][\u672F][\u6709][\u9650][\u516C][\u53F8][ ]{0,}'
    }
    for i in range(len(cookie['JSESSIONID'])):
        cookies = {
            'JSESSIONID': cookie['JSESSIONID'][i],
        }

        try:
            response = requests.post('http://123.233.113.66:8060/pubsearch/patentsearch/showSearchResult-startWa.shtml', headers=headers, cookies=cookies, data=data, proxies=proxies, verify=False)
            print(response.status_code)
            if response.status_code != 200:
                index.append(i)
            time.sleep(1)
        except Exception as e:
            print(e)
            time.sleep(1)

    with open('./data/invalid_cookies.json', 'w') as s:
        json.dump(index, s)


if __name__ == "__main__":
    main()
