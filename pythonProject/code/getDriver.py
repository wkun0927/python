# -*- coding: utf-8 -*-
# @Author            : 王琨
# @Email             : 18410065868@163.com
# @Date              : 2021-05-28 15:07:44
# @Last Modified by  : 王琨
# @Last Modified time: 2021-06-23 16:45:01
# @File Path         : D:\Dev\pythonProject\getDriver.py
# @Project Name      : pythonProject
# @Description       : 

from user_agent import generate_user_agent
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
            '--user-agent=' + generate_user_agent())
    options.add_argument('--hide-scrollbars')
    options.add_argument('--disable-bundled-ppapi-flash')
    options.add_argument('--mute-audio')
    # options.add_argument('--proxy-server=http:119.3.235.101:3128')
    driver = webdriver.Chrome(options=options,
                              executable_path='C:/Users/wk/AppData/Local/Google/Chrome/Application/chromedriver.exe')
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    })

    return driver
