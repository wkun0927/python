# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-09-28 09:43:32
# @Descripttion: 商标信息查询

import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from user_agent import generate_user_agent


def getDriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument('--headless')  # 无界面形式
    options.add_argument('--no-sandbox')  # 取消沙盒模式
    options.add_argument('--disable-setuid-sandbox')
    # options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--incognito')  # 启动进入隐身模式
    options.add_argument('--lang=zh-CN')  # 设置语言为简体中文
    options.add_argument(
        '--user-agent={}'.format(generate_user_agent()))
    options.add_argument('--hide-scrollbars')
    options.add_argument('--disable-bundled-ppapi-flash')
    options.add_argument('--mute-audio')
    # options.add_argument('--proxy-server={}'.format(proxy(headers)))  # 代理IP
    browser = webdriver.Chrome(options=options)
    browser.set_window_size(1920, 1080)
    browser.execute_cdp_cmd("Network.enable", {})
    browser.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => false
            })
        """
    })

    return browser


def main():
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"
    url = 'http://sbj.cnipa.gov.cn/'
    driver = getDriver()
    driver.get(url=url)
    WebDriverWait(driver, 15).until(lambda x: x.find_element(By.XPATH, '//*[@class="bscont12 bscont"]//a'))
    driver.find_element(By.XPATH, '//*[@class="bscont12 bscont"]//a').click()
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])
    WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, '//div[2]//div[2]//tr[2]/td[1]'))
    driver.find_element(By.XPATH, '//div[2]//div[2]//tr[2]/td[1]').click()
    time.sleep(10)


if __name__ == '__main__':
    main()
