# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-09-28 09:43:32
# @Descripttion: 商标信息查询

import random
import time

import requests
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def getDriver():
    options = webdriver.ChromeOptions()
    # prefs = {"profile.managed_default_content_settings.images": 2}
    # options.add_experimental_option("prefs", prefs)
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--ignore-ssl-errors")
    # options.add_argument('--headless')  # 无界面形式
    options.add_argument('--user-agent=' + UserAgent().random)
    # options.add_argument('--proxy-server={}'.format(get_proxies()))
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"
    browser = webdriver.Chrome(options=options)
    with open('C:/python/work/stealth.min.js') as f:
        js = f.read()
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
    })
    browser.maximize_window()
    return browser


def get_proxies():
    ip_url = "http://192.168.10.25:8000/ip"
    proxies = requests.get(ip_url, headers={'User-Agent': 'Mozilla/5.0'}).json()
    proxy = proxies['https'].split('@')[-1]
    return proxy


def main():
    url = 'http://sbj.cnipa.gov.cn/'
    driver = getDriver()
    driver.get(url=url)
    WebDriverWait(driver, 30).until(lambda x: x.find_element(By.XPATH, '//*[@class="bscont12 bscont"]//a'))
    driver.find_element(By.XPATH, '//*[@class="bscont12 bscont"]//a').click()
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])
    WebDriverWait(driver, 30).until(lambda x: x.find_element(By.XPATH, '//div[2]//div[2]//tr[2]/td[1]'))
    driver.find_element(By.XPATH, '//div[2]//div[2]//tr[2]/td[1]').click()
    time.sleep(10)


if __name__ == '__main__':
    main()
