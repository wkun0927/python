# -*- coding: utf-8 -*-
# @Author            : 王琨
# @Email             : 18410065868@163.com
# @Date              : 2021-06-16 10:10:45
# @Last Modified by  : 王琨
# @Last Modified time: 2021-06-23 16:46:25
# @File Path         : D:\Dev\pythonProject\小微企业名录.py
# @Project Name      : pythonProject
# @Description       : 

import time

import ipdb
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from user_agent import generate_user_agent
import re
from 小微企业_验证码 import get


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
    options.add_argument('--user-agent={}'.format(generate_user_agent()))
    options.add_argument('--hide-scrollbars')
    options.add_argument('--disable-bundled-ppapi-flash')
    options.add_argument('--mute-audio')
    # options.add_argument('--proxy-server={}'.format(proxy(headers)))
    browser = webdriver.Chrome(options=options, executable_path='C:/Users/18410/AppData/Local/Google/Chrome/Application/chromedriver.exe')
    browser.maximize_window()
    browser.execute_cdp_cmd("Network.enable", {})
    browser.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {"source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
            })
        """})

    return browser


def simulateDragX(self, source, x):
    """
    模仿人的拖拽动作：快速沿着X轴拖动（存在误差），再暂停，然后修正误差
    防止被检测为机器人，出现“图片被怪物吃掉了”等验证失败的情况
    :param source:要拖拽的html元素
    :param x: 拖拽目标x轴距离
    :return: None
    """
    action_chains = webdriver.ActionChains(self.driver)
    # 点击，准备拖拽
    action_chains.click_and_hold(source)

    # 总误差值
    for point in x:
        action_chains.move_by_offset(point[0], point[1])
        # 暂停一会
        action_chains.pause(self.__getRadomPauseScondes())
    action_chains.release()
    action_chains.perform()


def main(value):
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"
    driver = getDriver()

    url = 'http://xwqy.gsxt.gov.cn/'
    driver.get(url=url)

    # 点击“小微企业库”
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "小微企业库")]')))
    driver.find_element_by_xpath('//div[2]/ul/li[5]/a/span').click()
    time.sleep(5)

    # 输入企业名称
    driver.find_element_by_id('searchtitle').send_keys(value)
    driver.find_element_by_class_name('search_btn').click()  # 点击搜索
    WebDriverWait(driver, 10).until(lambda y: y.find_element_by_xpath('//div[5]/div[2]/div[2]/div[1]/div[2]/div[1]/a[1]/div[1]/div[1]'))
    full_url = driver.find_element_by_xpath('//div[5]/div[2]/div[2]/div[1]/div[2]/div[1]/a[1]/div[1]/div[1]').get_attribute('style')
    full_url = re.findall(r'"(.+?)"', full_url)[0]
    WebDriverWait(driver, 10).until(lambda z: z.find_element_by_xpath('//div[6]/div[2]/div[2]/div[1]/div[2]/div[1]/a[2]/div[1]/div[1]'))
    cut_url = driver.find_element_by_xpath('//div[6]/div[2]/div[2]/div[1]/div[2]/div[1]/a[2]/div[1]/div[1]').get_attribute('style')
    cut_url = re.findall(r'"(.+?)"', cut_url)[0]
    full = requests.get(full_url)
    cut = requests.get(cut_url)
    with open('./0.webp', 'wb') as f:
        f.write(full.content)
    with open('./1.webp', 'wb') as s:
        s.write(cut.content)

    info = get()
    html = driver.find_element_by_xpath('//div[6]/div[2]/div[2]/div[2]/div[2]')
    x = info['trace']
    simulateDragX(html, x)
    driver.find_element_by_xpath('//td[@class="td_cc"]/a').click()
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'main_con')))
    test = driver.find_element_by_xpath('//div[@class="main_con"]').get_attribute('textContent')

    print(test)
    driver.quit()


if __name__ == '__main__':
    name = '中国烟草总公司'
    main(name)
