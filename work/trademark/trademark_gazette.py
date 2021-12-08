# -*- coding: utf-8 -*-
# @Author              : 王琨
# @Date                : 2021-07-21 15:59:11
# @LastEditTime: 2021-12-06 16:24:12
# @LastEditors: Please set LastEditors
# @FilePath            : \pythonProject\trademark_gazette.py
# @Description         : 商标公告

import random
import time

import ipdb
import pyautogui
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from user_agent import generate_user_agent


def proxy(obj):
    while True:
        proxy_url = 'http://17610040106.v4.dailiyun.com/query.txt?key=NP86444E99&word=&count=1&rand=false&ltime=0&norepeat=false&detail=false'
        response = requests.get(proxy_url, headers=obj)
        proxies = response.text.strip()
        if proxies:
            break
        else:
            time.sleep(20)
    print(proxies)
    return proxies


def get_driver(obj):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument('--disable-blink-features=AutomationControlled')
    # options.add_argument('--headless')  # 无界面形式
    options.add_argument('--no-sandbox')  # 取消沙盒模式
    options.add_argument('--disable-setuid-sandbox')
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--incognito')  # 启动进入隐身模式
    options.add_argument('--lang=zh-CN')  # 设置语言为简体中文
    options.add_argument(
        '--user-agent=' + generate_user_agent())
    options.add_argument('--hide-scrollbars')
    options.add_argument('--disable-bundled-ppapi-flash')
    options.add_argument('--mute-audio')
    options.add_argument('--proxy-server={}'.format(proxy(obj)))
    browser = webdriver.Chrome(options=options)
    browser.execute_cdp_cmd("Network.enable", {})
    browser.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    with open('stealth.min.js') as f:
        js = f.read()
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
    })
    browser.implicitly_wait(10)

    return browser


url = 'http://sbj.cnipa.gov.cn/'
headers = {
    'user-agent': generate_user_agent()
}
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["pageLoadStrategy"] = "none"
driver = get_driver(headers)
driver.maximize_window()
driver.get(url)
# WebDriverWait(driver, 100).until(lambda x: x.find_element_by_xpath('//*[@class="bscont12 bscont"]'))
driver.find_element_by_xpath('//*[@class="bscont12 bscont"]//a').click()
time.sleep(50)
pyautogui.moveTo(575, 706, duration=2, tween=pyautogui.easeInOutQuad)
pyautogui.click()
ipdb.set_trace()
pyautogui.moveTo(1542, 656, duration=2, tween=pyautogui.easeInOutQuad)
pyautogui.click()
WebDriverWait(driver, 100).until(lambda x: x.find_element_by_xpath('//div[@id="list_shot"]//li[1]/img'))
driver.find_element_by_xpath('//div[@id="list_shot"]//li[1]/img').get_attribute('href')
