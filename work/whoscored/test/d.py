# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-12-14 16:06:15
# @Descripttion:

import random
import time

import requests
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait


def getDriver():
    options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    # options.add_argument("--disable-extensions")
    # options.add_argument("--disable-gpu")
    # options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument('--headless')  # 无界面形式
    # options.add_argument('--no-sandbox')  # 取消沙盒模式
    # options.add_argument('--disable-setuid-sandbox')
    # # options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument('--incognito')  # 启动进入隐身模式
    options.add_argument('--lang=zh-CN')  # 设置语言为简体中文
    options.add_argument('--user-agent=' + UserAgent().random)
    print(UserAgent().random)
    # options.add_argument('--hide-scrollbars')
    # options.add_argument('--disable-bundled-ppapi-flash')
    # options.add_argument('--mute-audio')
    # options.add_argument('--proxy-server={}'.format(get_proxies()))
    # options.add_extension(proxy_path)
    browser = webdriver.Chrome(options=options)
    with open('C:/python/work/stealth.min.js') as f:
        js = f.read()
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
    })
    browser.maximize_window()
    # browser.execute_cdp_cmd("Network.enable", {})
    # browser.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    # browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    #     "source": """
    #     Object.defineProperty(navigator, 'webdriver', {
    #         get: () => undefined
    #         })
    #     """
    # })
    return browser


def get_proxies():
    ip_url = "http://192.168.10.25:8000/ip"
    proxies = requests.get(ip_url, headers={'User-Agent': 'Mozilla/5.0'}).json()
    proxy = proxies['https'].split('@')[-1]
    return proxy


def main():
    # proxy_path = create_proxyauth_extension(
    #     proxy_host="proxy.crawlera.com",
    #     proxy_port=8010,
    #     proxy_username="fea687a8b2d448d5a5925ef1dca2ebe9",
    #     proxy_password=""
    # )
    url = 'https://bot.sannysoft.com/'
    driver = getDriver()
    driver.get(url)
    driver.save_screenshot('C:/python/work/whoscored/img/img.png')


if __name__ == "__main__":
    main()
