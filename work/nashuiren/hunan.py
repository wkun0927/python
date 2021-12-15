# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date:   2021-08-31 10:29:45
# @Last Modified by:   王琨
# @Last Modified time: 2021-08-31 11:42:32
# @Description: 湖南 数字字母验证码

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
    options.add_argument(
        '--user-agent=' + generate_user_agent())
    options.add_argument('--hide-scrollbars')
    options.add_argument('--disable-bundled-ppapi-flash')
    options.add_argument('--mute-audio')
    # options.add_argument('--proxy-server={}'.format(proxy(headers)))
    browser = webdriver.Chrome(options=options)
    browser.maximize_window()
    browser.execute_cdp_cmd("Network.enable", {})
    browser.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        "source": """low
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
            })
        """
    })

    return browser


def two_value():
    img = Image.open('./验证码图片/hunan_identifier.png')
    im = img.convert('L')
    low = 80
    top = 190
    table = []

    for j in range(256):
        if j < low or j > top:
            table.append(1)
        else:
            table.append(0)
    bim = im.point(table, '1')
    bim.save('./验证码图片/hunan_identifier.png')


def main(identifier):
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"
    url = 'http://hunan.chinatax.gov.cn/taxpayersearch/20190413003981'
    driver = getDriver()
    driver.get(url)
    WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//*[@id="sbh"]'))

    driver.find_element_by_xpath('//*[@id="sbh"]').send_keys(identifier)

    time.sleep(2)
    while True:
        # 截取验证码图片
        driver.save_screenshot('./验证码图片/hunan_picture.png')  # 全屏截图
        # 定位验证码在iframe中的坐标
        element = driver.find_element_by_id('codeImgGm')
        print(element.location)
        print(element.size)
        # 真实坐标需要加上iframe的坐标
        left = element.location['x']
        top = element.location['y']
        right = element.location['x'] + element.size['width']
        bottom = element.location['y'] + element.size['height']
        im = Image.open('./验证码图片/hunan_picture.png')
        im = im.crop((left, top, right, bottom))
        im.save('./验证码图片/hunan_identifier.png')

        # 识别验证码
        with open('./验证码图片/hunan_identifier.png', 'rb') as f:
            image = f.read()
        sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
        text = sdk.predict(image_bytes=image)
        print(text)
        # 输入验证码
        driver.find_element_by_xpath('//*[@id="yzm"]').send_keys(text)
        time.sleep(1)
        # 点击“查询”
        driver.find_element_by_xpath('//*[@id="creditlevelsearch"]/div[2]/div[1]').click()
        time.sleep(3)
        try:
            info = driver.find_element_by_xpath('//*[@id="resBody"]/tr').get_attribute('textContent')
        except NoSuchElementException:
            driver.find_element_by_xpath('//a[contains(text(), "确定")]').click()
            driver.find_element_by_xpath('//*[@id="yzm"]').clear()
            time.sleep(2)
            continue
        print(info)
        break

    driver.quit()


if __name__ == '__main__':
    ID = '91430111MA4R3MT0XN'
    main(ID)
