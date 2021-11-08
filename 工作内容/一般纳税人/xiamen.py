# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-08-30 09:38:40
# @LastEditors: 王琨
# @LastEditTime: 2021-08-30 09:39:02
# @FilePath: /python/工作内容/一般纳税人/xiamen.py
# @Description: 

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from user_agent import generate_user_agent
import requests
import time
import re
import os
from PIL import Image
import muggle_ocr


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
        '--user-agent=' + generate_user_agent())
    options.add_argument('--hide-scrollbars')
    options.add_argument('--disable-bundled-ppapi-flash')
    options.add_argument('--mute-audio')
    # options.add_argument('--proxy-server={}'.format(proxy(headers)))
    browser = webdriver.Chrome(options=options, executable_path='C:/Users/18410/AppData/Local/Google/Chrome/Application/chromedriver.exe')
    browser.maximize_window()
    browser.execute_cdp_cmd("Network.enable", {})
    browser.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
            })
        """
    })
    # with open('stealth.min.js') as f:
    #     js = f.read()
    # browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    #     "source": js
    # })
    # browser.implicitly_wait(10)

    return browser


def main():
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"
    url = 'https://etax.xiamen.chinatax.gov.cn:8443/bsfw/nsrgl/queryYbnsrzg.do'
    identifier = '91350211MA337MJ470'
    driver = getDriver()
    driver.get(url)
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="layui-layer1"]/div[3]/a').click()
    WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//td//tr[1]/td[2]/input'))
    time.sleep(1)

    driver.find_element_by_xpath('//td//tr[1]/td[2]/input').send_keys(identifier)

    time.sleep(2)

    while True:
        # 截取验证码图片
        driver.save_screenshot('./验证码图片/xiamen_picture.png')  # 全屏截图
        # 定位验证码在iframe中的坐标
        element = driver.find_element_by_id('imgcheckcode')
        print(element.location)
        print(element.size)
        # 真实坐标需要加上iframe的坐标
        left = element.location['x']
        top = element.location['y']
        right = element.location['x'] + element.size['width']
        bottom = element.location['y'] + element.size['height']
        im = Image.open('./验证码图片/xiamen_picture.png')
        im = im.crop((left, top, right, bottom))
        im.save('./验证码图片/xiamen_identifier.png')

        # 识别验证码
        with open('./验证码图片/xiamen_identifier.png', 'rb') as f:
            image = f.read()
        sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
        text = sdk.predict(image_bytes=image)
        print(text)
        # 输入验证码
        driver.find_element_by_xpath('//tr[2]//tr[3]/td[2]/input[1]').send_keys(text)
        time.sleep(1)
        # 点击查询
        driver.find_element_by_xpath('//input[@type="button"]').click()
        time.sleep(3)
        # 抓取数据
        info = driver.find_element_by_xpath('//div[@class="searchResult"]/table/tbody/tr[3]').get_attribute('textContent')
        if info == '没有符合条件的数据！':
            driver.find_element_by_xpath('//*[@id="layui-layer1"]/div[3]/a').click()
            driver.find_element_by_xpath('//tr[2]//tr[3]/td[2]/input[1]').clear()
            continue
        print(info)
        break

        # try:
        #     info = driver.find_element_by_xpath('//*[@id="dataTable"]/tbody/tr').get_attribute('textContent')
        #     print(info)
        #     break
        # except NoSuchElementException:
        #     driver.find_element_by_xpath('//*[@id="layui-layer4"]/div[3]/a').click()
        #     time.sleep(1)
        #     driver.find_element_by_xpath('//*[@id="imgYzm"]').click()
        #     time.sleep(3)
        #     continue

    driver.quit()


main()
