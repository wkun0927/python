# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date:   2021-05-28 15:14:39
# @Last Modified by:   王琨
# @Last Modified time: 2021-06-16 17:45:37
import time

import requests
from lxml import etree
import json
import getDriver

List = []
ICPNum = []
driver = getDriver.getDriver()

with open('comUrl.json', 'r') as f:
    comDick = json.loads(f.read().encode('utf-8'))

for name in comDick:
    Value = str(comDick[name])
    # print(Value)

    if Value == '没有官网':
        # print(name, Value)
        continue

    driver.get(Value)
    HTML = driver.page_source

    if "http://beian.miit.gov.cn/" in HTML:
        Num = driver.find_elements_by_xpath('//*[@href="http://beian.miit.gov.cn/"]')
    elif "http://beian.miit.gov.cn" in HTML:
        Num = driver.find_elements_by_xpath('//*[@href="http://beian.miit.gov.cn"]')
    elif "https://beian.miit.gov.cn/" in HTML:
        Num = driver.find_elements_by_xpath('//*[@href="https://beian.miit.gov.cn/"]')
    else:
        Num = driver.find_elements_by_xpath('//*[@href="https://beian.miit.gov.cn"]')

    for item in range(len(Num)):
        List.append(Num[item].get_attribute('textContent').strip())

    for i in List:
        if '网' in i:
            List.remove(i)

    for Num in List:
        if '-' in Num[-4:]:
            n = Num.find('-', -4, -1)
            rex = Num[n:]
            Num = Num.replace(rex, '')
        if '号' not in Num:
            Num = Num + '号'
    ICPNum.append(Num)
ICPNum = json.dumps(ICPNum)
with open('ICPNum.json', 'w') as f:
    f.write(ICPNum)
driver.quit()