# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date:   2021-05-18 17:17:04
# @Last Modified by:   王琨
# @Last Modified time: 2021-06-16 17:45:32
import time
import requests
import ipdb
from selenium import webdriver


def getDriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # options.add_argument('--headless')  # 无界面形式
    options.add_argument('--no-sandbox')  # 取消沙盒模式
    options.add_argument('--disable-setuid-sandbox')
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument('--incognito')  # 启动进入隐身模式
    options.add_argument('--lang=zh-CN')  # 设置语言为简体中文
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36')
    options.add_argument('--hide-scrollbars')
    options.add_argument('--disable-bundled-ppapi-flash')
    options.add_argument('--mute-audio')

    driver = webdriver.Chrome(options=options,
                              executable_path='C:/Users/wk/AppData/Local/Google/Chrome/Application/chromedriver.exe')
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })

    return driver


List = []


def getBeianInfo():


    try:
        # 尝试获取备案信息
        Name = driver.find_element_by_xpath('//*[@class="has-gutter"]').get_attribute('textContent')
        List.append(Name)
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
    except:
        print(List)
        return 0

    try:
        driver.find_element_by_xpath('//*[@class="btn-next"]').click()
        time.sleep(10)
        getBeianInfo()
    finally:
        driver.quit()


value = input('请输入公司名称：')
driver = getDriver()
Url = 'https://www.baidu.com/'
# 打开百度首页
driver.get(Url)
# 输入
driver.find_element_by_id('kw').send_keys(value)
# 点击
driver.find_element_by_id('su').click()
# 延迟5秒，等待加载。
time.sleep(5)
# 定位官网链接地址
res = driver.find_element_by_xpath('//*[@id="1"]/h3/a[1]')
try:
    chk = driver.find_element_by_xpath('//*[@id="1"]/h3/a[2]').get_attribute('href')
    if chk == 'http://trust.baidu.com/vstar/official/intro?type=gw' or chk == 'https://trust.baidu.com/vstar/official/intro?type=gw':
        # 获得该官网在百度的URL
        pageUrl = res.get_attribute('href')
        driver.quit()
        # 打开新的网页
        driver = getDriver()
        # driver = webdriver.Chrome(executable_path='C:/Users/wk/AppData/Local/Google/Chrome/Application/chromedriver.exe')
        driver.get(pageUrl)
        # 获得官网真正的URL
        URL = driver.current_url
        # 官网名称
        Title = driver.title
        # 备案号
        try:
            rec = driver.find_element_by_xpath('//*[@href="http://beian.miit.gov.cn/"]').get_attribute('textContent').strip()
        except:
            rec = driver.find_element_by_xpath('//*[@href="https://beian.miit.gov.cn/"]').get_attribute('textContent').strip()
        if '-' in rec[-4:-1]:
            n = rec.find('-')
            rex = rec[n:]
            rec = rec.replace(rex, '')
        if '号' not in rec:
            rec = rec + '号'

        # 进入ICP备案管理系统网站查询审核时间
        miitUrl = "http://beian.miit.gov.cn/"
        driver = getDriver()
        driver.get(miitUrl)
        time.sleep(15)
        driver.find_element_by_xpath('//*[@id="app"]/div/header/div[3]/div/div/input').send_keys(rec)
        time.sleep(5)
        print(URL, Title, rec, '\n')
        ipdb.set_trace()
        getBeianInfo()

    else:
        driver.quit()
        print('该公司没有官网')
except:
    driver.quit()
    print('该公司没有官网')
