# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date:   2021-05-28 10:21:08
# @Last Modified by:   王琨
# @Last Modified time: 2021-06-16 17:45:40
import time
import json
import getDriver

Company = {}
driver = getDriver.getDriver()
Url = 'https://www.baidu.com'
driver.get(Url)
time.sleep(2)
x = 1
while x:
    value = eval(input('输入：'))
    for item in value:
        if item == '0':
            x = 0
            break
        driver.find_element_by_id('kw').send_keys(item)
        driver.find_element_by_id('su').click()
        time.sleep(5)
        Address = ['//*[@href="http://trust.baidu.com/vstar/official/intro?type=gw"]',
                   '//*[@href="https://trust.baidu.com/vstar/official/intro?type=gw"]']
        try:
            try:
                res = driver.find_element_by_xpath(Address[0] + '/../a[1]').get_attribute('href')
            except:
                res = driver.find_element_by_xpath(Address[1] + '/../a[1]').get_attribute('href')
            Company[item] = res
        except:
            Company[item] = '没有官网'
        driver.find_element_by_id('kw').clear()
jsObj = json.dumps(Company)
with open('comUrl.json', 'w') as f:
    f.write(jsObj)
driver.quit()
