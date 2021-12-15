# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-08-27 17:06:40
# @LastEditors: 王琨
# @LastEditTime: 2021-08-27 17:06:53
# @FilePath: /python/工作内容/一般纳税人/ningbo.py
# @Description: 宁波

import os
import re
import time

import muggle_ocr
import requests
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
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
    options.add_argument('--user-agent=' + generate_user_agent())
    options.add_argument('--hide-scrollbars')
    options.add_argument('--disable-bundled-ppapi-flash')
    options.add_argument('--mute-audio')
    # options.add_argument('--proxy-server={}'.format(proxy(headers)))
    browser = webdriver.Chrome(options=options)
    browser.maximize_window()
    browser.execute_cdp_cmd("Network.enable", {})
    browser.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {"source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
            })
        """})

    return browser


def main(identifier, Name):
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"
    url = 'https://etax.ningbo.chinatax.gov.cn/yhs-web/cxzx/index.html?&code=ybnsrzgcx&id=840#/ybnsrzgcx'
    driver = getDriver()
    driver.get(url)
    WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//input[@name="nsrsbh"]'))
    src = driver.find_element_by_xpath('//*[@class="yzm"]').get_attribute('src')
    print(src)
    headers = {
        'Connection': 'close',
        'user-agent': generate_user_agent()
    }
    res = requests.get('https://etax.ningbo.chinatax.gov.cn/yhs-web/api/yhsyzm/get?1631008417224', headers=headers, )
    print(res.status_code)
    with open('./src.jpg', 'wb') as f:
        f.write(res.content)
    import ipdb
    ipdb.set_trace()

    # driver.find_element_by_xpath('//input[@name="nsrsbh"]').send_keys(identifier)
    # driver.find_element_by_xpath('//input[@name="nsrmc"]').send_keys(Name)

    time.sleep(2)
    while True:
        # 截取验证码图片
        driver.save_screenshot('./验证码图片/ningbo_picture.png')  # 全屏截图
        # 定位验证码在iframe中的坐标
        element = driver.find_element_by_xpath('//*[@class="yzm"]')
        print(element.location)
        print(element.size)
        # 真实坐标需要加上iframe的坐标
        left = element.location['x']
        top = element.location['y']
        right = element.location['x'] + element.size['width']
        bottom = element.location['y'] + element.size['height']
        im = Image.open('./验证码图片/ningbo_picture.png')
        im = im.crop((left, top, right, bottom))
        im.save('./验证码图片/ningbo_identifier.png')

        # 识别验证码
        with open('./验证码图片/ningbo_identifier.png', 'rb') as f:
            image = f.read()
        sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
        text = sdk.predict(image_bytes=image)
        print(text)
        # 输入验证码
        driver.find_element_by_xpath('//*[@name="yzm"]').send_keys(text)
        try:
            driver.find_element_by_xpath('//*[@id="app"]//div[2]//div[3]//p').get_attribute('textContent')
            driver.find_element_by_xpath('//*[@class="yzm"]').click()
            continue
        except NoSuchElementException:
            pass
        time.sleep(1)
        # 点击“查询”
        driver.find_element_by_xpath('//span[contains(text(), "查 询")]').click()
        time.sleep(3)
        info = driver.find_element_by_xpath('//tr[@class="ant-table-row "]').get_attribute('textContent')
        print(info)
        break

    driver.quit()


if __name__ == '__main__':
    ID = '9133020114479257XW'
    name = '宁波方太厨具有限公司'
    main(ID, name)
