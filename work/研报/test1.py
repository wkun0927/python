# encoding=utf-8

# 'stock_list', '600549'  修改这个股票代码即可


import requests
import json


def get_proxy():  # ip代理
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4068.4 Safari/537.36'
    }
    url = 'http://17610040106.v4.dailiyun.com/query.txt?key=NP86444E99&word=&count=1&rand=false&ltime=0&norepeat=false&detail=false'
    response = requests.get(url, headers=headers)
    proxy_dly = response.text.strip()
    # print(proxy_dly)
    if proxy_dly:
        proxies = {
            "http": "http://" + proxy_dly,
            "https": "http://" + proxy_dly
        }
        return proxies


def get_url(stock, i=1):  # 获取研报标题和url
    params = (
        ('page_size', '50'),
        ('page_index', 1),
        ('ann_type', 'A'),
        ('client_source', 'web'),
        ('stock_list', stock),
    )

    response = requests.get('http://np-anotice-stock.eastmoney.com/api/security/ann', params=params, verify=False)
    # print(response.text)      .replace('jQuery112309296665354138134_1626056918998(','')[:-1]
    result = response.text
    result = json.loads(result)
    # print(result)

    url_prefix = 'http://data.eastmoney.com/notices/detail/' + stock + '/'
    for i in range(0, 10):
        print(result['data']['list'][i]['title'])
        # print(result['data']['list'][i]['notice_date'])
        # print(result['data']['list'][i]['display_time'])
        art_code = result['data']['list'][i]['art_code']
        print(url_prefix + str(art_code) + '.html')


if __name__ == '__main__':
    stock = '000762'
    try:
        for i in range(1, 5):
            get_url(stock, i)
    except:
        pass
