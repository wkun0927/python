# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-08-09 20:39:37
# @Description: 新浪财经网

import csv
import requests
from lxml import etree
from user_agent import generate_user_agent

headers = {
    'User-Agent': generate_user_agent(),
}
KEY = input('请输入类型：')
CODE = input('请输入股票代码：')
urls = {
    'A股': 'http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/' + CODE + '/displaytype/4.phtml',
    'H股': 'https://stock.finance.sina.com.cn/hkstock/finance/' + CODE + '.html#a1',
}
url = urls[KEY]
response = requests.get(url=url, headers=headers)
html = etree.HTML(response.text)
File = []
count = 1
count1 = 1
count2 = 1
count3 = 1
while True:
    List = []
    result = html.xpath('//table[@id="BalanceSheetNewTable0"]/tbody/tr[' + str(count) + ']//text()')
    for row in result:
        List.append(row)
    print(List)
    if not List:
        TH = html.xpath('//tbody[@id="tableGetFinanceStandard"]/tr[' + str(count) + ']/th/text()')
        result = html.xpath('//tbody[@id="tableGetFinanceStandard"]/tr[' + str(count) + ']/td/text()')
        if not TH:
            TH = html.xpath('//tbody[@id="tableGetBalanceSheet"]/tr[' + str(count1) + ']/th/text()')
            result = html.xpath('//tbody[@id="tableGetBalanceSheet"]/tr[' + str(count1) + ']/td/text()')
            count1 += 1
            if not TH:
                TH = html.xpath('//tbody[@id="tableGetCashFlow"]/tr[' + str(count2) + ']/th/text()')
                result = html.xpath('//tbody[@id="tableGetCashFlow"]/tr[' + str(count2) + ']/td/text()')
                count2 += 1
                if not TH:
                    TH = html.xpath('//tbody[@id="tableGetFinanceStatus"]/tr[' + str(count3) + ']/th/text()')
                    result = html.xpath('//tbody[@id="tableGetFinanceStatus"]/tr[' + str(count3) + ']/td/text()')
                    count3 += 1
                    if not TH:
                        break
        List.append(TH[0])
        for row in result:
            List.append(row)
    print(List)
    File.append(List)
    count += 1
print(File)

with open('Financial.csv', 'w', newline='') as f:
    f_csv = csv.writer(f)
    f_csv.writerows(File)
