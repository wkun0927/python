import csv
import time

import requests
import json

with open('./data/cookies.json') as f:
    cookie = json.load(f)
    print(cookie['JSESSIONID'][0])

page_num = 14000
cookies = {
    # 'IS_LOGIN': 'true',
    # 'WEE_SID': '18B2E0ABC0373F90FC2AE1DC2CEC055B.pubsearch02',
    'JSESSIONID': cookie['JSESSIONID'][0],
    # 'avoid_declare': 'declare_pass',
    # 'Anonymity_SearchHistory_SessionId': '20D21AEEFAA4F4BD28FB7E78C61C1BC8.pubsearch02',
    # 'Anonymity_SearchHistory': '',
}

start = time.time()
for i in range(page_num):
    print(i)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
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
        'resultPagination.start': str(i * 12),
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
    try:
        response = requests.post('http://123.233.113.66:8060/pubsearch/patentsearch/showSearchResult-startWa.shtml', headers=headers, cookies=cookies, data=data, verify=False)
        print(response.status_code)
        if response.status_code != 200:
            begin = time.time()
            print(begin-start)
            break
        info = response.json()
        data = info['searchResultDTO']['searchResultRecord']
        print(len(data))
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
