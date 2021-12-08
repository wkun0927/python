# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-10-13 16:33:48
# @Descripttion:

import csv
import time

import requests


def get_proxies():
    ip_url = "http://192.168.10.25:8000/ip"
    proxies = requests.get(ip_url, headers={'User-Agent': 'Mozilla/5.0'}).json()
    print(proxies['http'])
    return proxies

page_num = 1
cookies = {
    # 'IS_LOGIN': 'true',
    # 'WEE_SID': '18B2E0ABC0373F90FC2AE1DC2CEC055B.pubsearch02',
    'JSESSIONID': '3AE40E957028CBA92BEC5ABEFFEC27FA.pubsearch02',
    # 'avoid_declare': 'declare_pass',
    # 'Anonymity_SearchHistory_SessionId': '20D21AEEFAA4F4BD28FB7E78C61C1BC8.pubsearch02',
    # 'Anonymity_SearchHistory': '',
}

for i in range(page_num):
    List = []
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'http://60.166.52.165:8030',
        'Referer': 'http://60.166.52.165:8030/patentsearch/tableSearch-showTableSearchIndex.shtml',
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
        response = requests.post('http://60.166.52.165:8030/pubsearch/patentsearch/tableSearch-showTableSearchIndex.shtml', headers=headers, cookies=cookies, proxies=get_proxies(), data=data, verify=False)
        print(response.status_code)
        info = response.json()
        for j in range(12):
            time.sleep(3)
            Dict = {}
            data = info['searchResultDTO']['searchResultRecord'][j]
            request_no = data['fieldMap']['APO']  # 申请号
            request_no_p = data['fieldMap']['AP']  # 申请号不带点
            request_date = data['fieldMap']['APD']  # 申请日
            public_no = data['fieldMap']['PN']  # 公开（公告）号
            public_date = data['fieldMap']['PD']  # 公开(公告）日
            patent_title = data['fieldMap']['TIVIEW']  # 专利标题
            ipc = data['fieldMap']['ICST']  # IPC分类号
            request_body = data['fieldMap']['PAVIEW']  # 申请/专利权人
            inventor = data['fieldMap']['INVIEW']  # 发明/设计人
            priority = data['fieldMap']['PR']  # 优先权号
            priority_date = data['fieldMap']['PRD']  # 优先权日
            proxy = data['fieldMap']['AGT']  # 代理人
            proxy_org = data['fieldMap']['AGY']  # 代理机构
            # abstract_url = data['absImgTI']['ABSIMG']  # 摘要附图
            type = data['fieldMap']['INT_VALUE']  # 专利类型；1发明，2实用，3外观
            # abstract =  # 专利摘要
            Applicant_Code = data['fieldMap']['AZ']  # 申请人邮编
            request_addr = data['fieldMap']['AA']  # 申请人地址
            申请人所在国_省 = data['fieldMap']['AC']
            外观设计洛迦诺分类号 = data['fieldMap']['LOCARNO']  # 外观设计洛迦诺分类号
            pnum = data['fieldMap']['PNUM']  # 引证
            fnum = data['fieldMap']['FNUM']  # 同族

            Dict['request_no'] = request_no
            Dict['request_date'] = request_date
            Dict['public_no'] = public_no
            Dict['public_date'] = public_date
            Dict['patent_title'] = patent_title
            Dict['ipc'] = ipc
            Dict['request_body'] = request_body
            Dict['inventor'] = inventor
            Dict['priority'] = priority
            Dict['priority_date'] = priority_date
            Dict['proxy'] = proxy
            Dict['proxy_org'] = proxy_org
            # Dict['abstract_url'] = abstract_url
            Dict['type'] = type
            Dict['Applicant_Code'] = Applicant_Code
            Dict['申请人所在国_省'] = 申请人所在国_省
            Dict['外观设计洛迦诺分类号'] = 外观设计洛迦诺分类号
            Dict['PNUM'] = pnum
            Dict['FNUM'] = fnum
            List.append(Dict)
    except Exception as e:
        print(e)
    print(List, len(List))
