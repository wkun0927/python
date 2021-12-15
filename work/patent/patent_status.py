# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-10-14 15:53:03
# @Descripttion: 法律状态

import requests


def str_insert(str_origin, pos, str_add):  # pos:索引，str_add:要添加的字符串
    str_list = list(str_origin)  # 字符串转list
    str_list.insert(pos, str_add)  # 在指定位置插入字符串
    str_out = ''.join(str_list)  # 空字符连接
    return str_out


def main():
    cookies = {
        'WEE_SID': 'B8285767D16CC54CF883BFB454C6CCB2.pubsearch01',
        'IS_LOGIN': 'true',
        'wee_username': 'a2Vyd2luMjc%3D',
        'wee_password': 'S2Vyd2luOTI3ODI2QA%3D%3D',
        'JSESSIONID': 'B8285767D16CC54CF883BFB454C6CCB2.pubsearch01',
        'avoid_declare': 'declare_pass',
        'Anonymity_SearchHistory_SessionId': '20D21AEEFAA4F4BD28FB7E78C61C1BC8.pubsearch02',
        'Anonymity_SearchHistory': '',
    }

    headers = {
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'http://123.233.113.66:8060',
        'Referer': 'http://123.233.113.66:8060/pubsearch/patentsearch/showViewList-jumpToView.shtml',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    }

    data = {'lawState.nrdPn': 'CN107342842A',
            'lawState.nrdAn': 'CN201610664987',
            'wee.bizlog.modulelevel': '0202201',
            'pagination.start': '0'}

    response = requests.post('http://123.233.113.66:8060/pubsearch/patentsearch/searchLawState-showPage.shtml', headers=headers, cookies=cookies, data=data, verify=False)
    info = response.json()
    Dict = {}
    for i in range(3):
        try:
            Details = info['lawStateList'][i]
            key = Details['lawStateCNMeaning']  # 法律状态含义
            value = Details['prsDate']  # 法律状态公告日
            value = str_insert(value, 6, '-')
            value = str_insert(value, 4, '-')
            Dict[key] = value
        except IndexError:
            break

    print(Dict)


if __name__ == '__main__':
    main()
