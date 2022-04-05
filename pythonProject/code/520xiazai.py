from email import header
import requests
from lxml import etree
import re
from fake_useragent import UserAgent
import time
import json

url = 'http://www.51xiazai.cn/sort/'
headers = {'User-Agent': UserAgent().random}
response = requests.get(url, headers=headers)
html = etree.HTML(response.content.decode('utf-8'))
url_list = []
nums = 0
for i in range(1, 23):
    count = 1
    while count > 0:
        try:
            url_1 = html.xpath('//div[5]/div/div[' + str(i) + ']/div[2]/ul/li[' + str(count) + ']/a/@href')[0]
            url_list.append(url_1)
            count += 1
        except Exception as e:
            print(e)
            count = -1

for url in url_list:
    try:
        response1 = requests.get(url, headers=headers, cookies=cookies, verify=False)
        x = etree.HTML(response1.content.decode('utf-8'))
        num = x.xpath('//div[5]/div/div[1]/div[3]/div/span/text()')[0]
        num = re.findall(r"\d+?\d*", num)[0]
        print('num=', num)
        nums += int(num)
    except Exception as e:
        print(e)
        continue

print('nums=', nums * 25)
