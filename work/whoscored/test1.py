# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-12-09 19:09:19
# @Descripttion:

import requests

headers = {
    'authority': 'www.whoscored.com',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'visid_incap_774904=FwijbxU3SP2gBAMcA2UurKXTsWEAAAAAQUIPAAAAAABUHRXvJDC+zqFM7SPETJWD; incap_ses_431_774904=tqP/EyxcLgV1VKjiqzj7BaXTsWEAAAAAoSAq6nbOZ9AxWBQzQtjLuQ==; _ga=GA1.2.1018197862.1639044038; _gid=GA1.2.1826355566.1639044038; __qca=P0-1244411035-1639044022805; _xpid=3376547895; _xpkey=ghFwMUfbwD8PazhfqQBD7Tog7G1BH0kh; ct=HK',
}

response = requests.get('https://www.whoscored.com/', headers=headers)
