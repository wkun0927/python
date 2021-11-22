# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-10-11 18:48:52
# @Descripttion: 国家知识产权局专利网

import time

import pysnooper
import requests
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from user_agent import generate_user_agent


def getDriver(headers):
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
    options.add_argument('--user-agent={}'.format(generate_user_agent()))
    options.add_argument('--hide-scrollbars')
    options.add_argument('--disable-bundled-ppapi-flash')
    options.add_argument('--mute-audio')
    # options.add_argument('--proxy-server={}'.format(proxy(headers)))  # 代理IP
    browser = webdriver.Chrome(options=options, executable_path='C:/Program Files/Google/Chrome/Application/chromedriver.exe')
    browser.execute_cdp_cmd("Network.enable", {})
    browser.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {"source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => false
            })
        """})

    return browser


def main():
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"
    url = 'http://www.cnipa.gov.cn/'
    headers = {
        'user-agent': generate_user_agent()
    }
    driver = getDriver(headers=headers)
    driver.get(url)
    WebDriverWait(driver, 100).until(lambda x: x.find_element(By.XPATH, '//*[@id="barrierfree_container"]/div[3]/div[7]/dl/dd[1]/ul/li[6]/a'))
    retrieval = driver.find_element(By.XPATH, '//*[@id="barrierfree_container"]/div[3]/div[7]/dl/dd[1]/ul/li[6]/a')
    ActionChains(driver).move_to_element(retrieval).click().perform()
    time.sleep(1)
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])
    WebDriverWait(driver, 100).until(lambda x: x.find_element(By.XPATH, '//div[3]/div/div[3]/div[1]/a[1]'))
    agree = driver.find_element(By.XPATH, '//div[3]/div/div[3]/div[1]/a[1]')
    ActionChains(driver).move_to_element(agree).click().perform()
    WebDriverWait(driver, 100).until(lambda x: x.find_element(By.XPATH, '//div[1]/div[1]/div/div[1]/p/a[1]'))
    login = driver.find_element(By.XPATH, '//div[1]/div[1]/div/div[1]/p/a[1]')
    ActionChains(driver).move_to_element(login).click().perform()
    time.sleep(10)


if __name__ == "__main__":
    main()
