# -*- coding: utf-8 -*-
# @Author            : 王琨
# @Email             : 18410065868@163.com
# @Date              : 2021-06-07 18:02:47
# @Last Modified by  : 王琨
# @Last Modified time: 2021-06-24 09:13:07
# @File Path         : D:\Dev\pythonProject\Patent.py
# @Project Name      : pythonProject
# @Description       : 专利

import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import ipdb
import ip_api
from user_agent import generate_user_agent

proxy = ip_api.proxy()


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
            '--user-agent=' + generate_user_agent())
    options.add_argument('--hide-scrollbars')
    options.add_argument('--disable-bundled-ppapi-flash')
    options.add_argument('--mute-audio')
    # options.add_argument('--proxy-server=https://' + proxy)
    driver = webdriver.Chrome(options=options,
                              executable_path='C:/Program Files/Google/Chrome/Application/chromedriver.exe')
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    })

    return driver


# 打开浏览器
driver = getDriver()

# 打开网址，直到检测到登录按钮加载出来
first_url = 'https://www.cnipa.gov.cn/'
driver.get(first_url)
time.sleep(5)
driver.find_element_by_xpath('//a[@title="专利检索"]').click()
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'btnLogin')))
driver.find_element_by_id('btnLogin').click()
time.sleep(15)

# 输入账号密码
driver.find_element_by_xpath('//input[@name="username"]').send_keys('kerwin27')
driver.find_element_by_xpath('//input[@name="password"]').send_keys('2726kerwin')
ipdb.set_trace()

# 检测到输入框加载完成，输入查询条件并查询
WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.ID, 'keywords')))
value = input('请输入：')
driver.find_element_by_id('keywords').send_keys(value)
driver.find_element_by_id('keywords').send_keys(Keys.ENTER)
