# -*- coding: utf-8 -*-
# @Time : 2021/7/7-17:43
# @Author : Warren
# @Email : 18410065868@163.com
# @File : trademark_req.py
# @Project : pythonProject
# @Description : 使用requests请求

import requests


def get_proxies():
    ip_url = "http://152.136.208.143:5000/w/ip/random"
    proxies = requests.get(ip_url, headers={'User-Agent': 'Mozilla/5.0'}).json()
    return proxies


cookies = {
    'goN9uW4i0iKzS': '52WC8v5qsUAUr.MWCyekLyBAPSONE8JO3EbShvXw3vz4sEpcK98ve7OPFpVFjzt09kcmNZJHyR7UuqFuqDK6I1a',
    'UM_distinctid': '17c2bb7fe8f622-03bb7674cf5577-513c1743-144000-17c2bb7fe90f12',
    '__tads_uuid': '17B1B-006163D2BB',
    '_trs_uv': 'kumh6tqu_4693_iobt',
    '_va_id': '92ce04b101672b5d.1633945880.12.1634269705.1634269705.',
    '_va_ref': '%5B%22%22%2C%22%22%2C1634269705%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D',
    'ras_cookie3': '2272.7689.7938.0000',
    'JSESSIONID': '42574A86C930C136F1D481A02F77CEAF',
    'tmrpToken': 'F3151C0BE32AF8C6CD7640D5D80D6890',
    'goN9uW4i0iKzT': '53K0U_DmzDUlqqqmZ9OJ70a3Hho0C_94.Osf35_9aW_K4ckIuPrSmZGgkrIRL37bNvks7HjTYT42HRTQCHGlyHmXmn_jL.w3L9zDwl0xrCkltKEgM9H3qWIikKE2cbi5BC0ncWo3EEXnCLl7e3ntOGO498FOSxg6oB7xn3qLCVhF9GgTcMrC49fC7eOCcdtXkOti0dBHc5B3TaiAYMQE_p8Vo5STQrURlzNrpZbHusYKZilYhPD0qSopByKGcukH2EYRQWN63QH1k6.EbV7NseDjEZVfw33O3ljBTNRl0F92RkX_rTe7LseAml4.oSEcA9',
}

headers = {
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'http://wcjs.sbj.cnipa.gov.cn',
    'Referer': 'http://wcjs.sbj.cnipa.gov.cn/txnRead01.do?RyPaGY3r=qqr4yw.YtEqarhUeJ0udDhpl.nWAYdaK3oG6ECZQbQJgaYsn9x2XBlUldv8AQumZ6mqvvZt7sD.t878PqvIiDMWwOFQ8Ww74kRzrFiYKPg19oHQ0gEdj1ju6nA6Y8RZYUUXeTXFU63WQTfT0yCVqc68fAkV',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
}

params = (
    ('O56fzBVE', '5c.eENunbbNURK86wvZxAZnrLI97eowU7mTh1Jki_yQ1ULuqzSBgewYlXXYuNXS.X1oYk2zjs.C9eYL6GkTQD67x9STW0XCqROXwkKyW1B8zz6.tH17BnpjUmmsDvElZmuVLdWLJjBWbivZVjlW.oKLMteZS9_.CxK.sxEnYmR5iwKlfpxrvMVKKNy4vJDLVbz321Igzsr.XsXlYJNDpNhKxMN94mTsHndI2zs7kY1r37Lhqvjc0AnX73qn_lu5HYYvSxG6emyY.y4qsVrs2X1CnRKl5EXsycuX.sY.MlPn.R_s259p2d9K8DKQvZe6ry.xpJ8KMZVMtJ_p.q9vFub8yi3F80YKO8NQTSlQN2JoG'),
)

data = {
  'request:queryType': '',
  'request:queryAuto': '',
  'request:queryMode': '',
  'request:queryCom': '1',
  'request:mn': '',
  'request:ncs': '',
  'request:nc': '',
  'request:hnc': '\u534E\u4E3A\u6280\u672F\u6709\u9650\u516C\u53F8',
  'request:hne': '',
  'request:sn': '',
  'request:imf': '',
  'request:maxHint': '',
  'request:queryExp': 'hncc = \u534E\u4E3A\u6280\u672F\u6709\u9650\u516C\u53F8* ',
  'request:mi': 'D9B847543ADB8814225C711ADFDB27BE',
  'request:tlong': 'TUXlEln0SFaJexQDukIGJWqtNaqifZOk5VKI4BCtwQddXvjrQ4HX+2oc2X8sUFW5',
  'attribute-node:record_cache-flag': 'false',
  'attribute-node:record_start-row': '101',
  'attribute-node:record_page-row': '50',
  'attribute-node:record_sort-column': 'RELEVANCE',
  'attribute-node:record_page': '3'
}

response = requests.post('http://wcjs.sbj.cnipa.gov.cn/txnRead02.ajax', headers=headers, params=params, cookies=cookies, data=data, verify=False, proxies=get_proxies())

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.post('http://wcjs.sbj.cnipa.gov.cn/txnRead02.ajax?O56fzBVE=5c.eENunbbNURK86wvZxAZnrLI97eowU7mTh1Jki_yQ1ULuqzSBgewYlXXYuNXS.X1oYk2zjs.C9eYL6GkTQD67x9STW0XCqROXwkKyW1B8zz6.tH17BnpjUmmsDvElZmuVLdWLJjBWbivZVjlW.oKLMteZS9_.CxK.sxEnYmR5iwKlfpxrvMVKKNy4vJDLVbz321Igzsr.XsXlYJNDpNhKxMN94mTsHndI2zs7kY1r37Lhqvjc0AnX73qn_lu5HYYvSxG6emyY.y4qsVrs2X1CnRKl5EXsycuX.sY.MlPn.R_s259p2d9K8DKQvZe6ry.xpJ8KMZVMtJ_p.q9vFub8yi3F80YKO8NQTSlQN2JoG', headers=headers, cookies=cookies, data=data, verify=False)
print(response.content.decode('utf-8'))
