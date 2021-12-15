# -*- coding: utf-8 -*-
# @Author            : 王琨
# @Email             : 18410065868@163.com
# @Date              : 2021-05-31 11:13:01
# @Last Modified by  : 王琨
# @Last Modified time: 2021-06-23 16:45:41
# @File Path         : D:\Dev\pythonProject\ICPCheck.py
# @Project Name      : pythonProject
# @Description       : 

import csv
import json
import time

import ipdb
from PIL import Image
import getDriver


def getBeianInfo():
    try:
        for row in range(5):
            List1 = []
            List2 = []
            # 序号从1开始
            row = str(row + 1)
            for col in range(9):
                col = str(col + 1)
                # 单行
                rec1 = driver.find_element_by_xpath('//*[@class="el-table__body-wrapper is-scrolling-none"]'
                                                    '//*[@class="el-table__row warning-row"][' + row + ']//*['
                                                    + col + ']').get_attribute('textContent')
                List1.append(rec1)

            for col in range(9):
                col = str(col + 1)
                # 双行
                rec2 = driver.find_element_by_xpath('//*[@class="el-table__body-wrapper is-scrolling-none"]'
                                                    '//*[@class="el-table__row"][' + row + ']//*[' + col + ']'
                                                    ).get_attribute('textContent')
                List2.append(rec2)
            List.append(List1)
            List.append(List2)
        HTML = driver.find_element_by_xpath('//*[@class="btn-next"]').get_attribute('outerHTML')
        # print(HTML, '\n', type(HTML))
        if 'disable' not in HTML:
            driver.find_element_by_xpath('//*[@class="btn-next"]').click()
            time.sleep(5)
            getBeianInfo()
    except:
        print(List)
        return 0


# 公司名称
ICPNum = eval(input('请输入：'))
# with open('ICPNum.json', 'r') as f:
#     ICPNum = json.loads(f.read().encode('utf-8'))
List = []
driver = getDriver.getDriver()
driver.maximize_window()
miitUrl = "http://beian.miit.gov.cn/"
Title = ['序号', '主办单位名称', '主办单位性质', '网站备案号', '网站名称', '网站首页', '审核日期', '是否限制接入', '操作']
for rec in ICPNum:
    driver.get(miitUrl)
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="app"]/div/header/div[3]/div/div/input').send_keys(rec)
    driver.find_element_by_xpath('//*[@class="el-button el-button--primary"]').click()
    time.sleep(5)
    ipdb.set_trace()
    driver.save_screenshot('capture.png')
    ele = driver.find_element_by_id('bgImg')
    ele.screenshot('ele.png')
    getBeianInfo()

with open('ICPInfo.csv', 'w', newline='') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(Title)
    f_csv.writerows(List)
driver.quit()

# ['华为技术有限公司','深圳市腾讯计算机系统有限公司']