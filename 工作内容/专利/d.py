#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-11-10 09:32:16
# @Descripttion:

import cv2 as cv
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from user_agent import generate_user_agent


def getDriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--headless')  # 无界面形式
    options.add_argument('--no-sandbox')  # 取消沙盒模式
    options.add_argument('--disable-setuid-sandbox')
    # options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--incognito')  # 启动进入隐身模式
    options.add_argument('--lang=zh-CN')  # 设置语言为简体中文
    options.add_argument('--user-agent=' + generate_user_agent())
    options.add_argument('--hide-scrollbars')
    options.add_argument('--disable-bundled-ppapi-flash')
    options.add_argument('--mute-audio')
    # options.add_argument('--proxy-server={}'.format(get_proxies()))
    browser = webdriver.Chrome(options=options)
    browser.set_window_size(1920, 1080)
    browser.execute_cdp_cmd("Network.enable", {})
    browser.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {"source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
            })
        """})

    return browser


def main():
    url = 'http://123.233.113.66:8060/pubsearch/portal/uilogin-forwardLogin.shtml'
    driver = getDriver()
    driver.get(url)
    WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, '//*[@id="j_username"]'))
    # 截图识别验证码
    img = driver.find_element(By.XPATH, '//*[@id="codePic"]')
    driver.save_screenshot('./img/full.png')
    left = img.location['x']
    top = img.location['y']
    right = img.location['x'] + img.size['width']
    bottom = img.location['y'] + img.size['height']
    im = Image.open('./img/full.png')
    im = im.crop((left, top, right, bottom))
    im.save('./img/cut.png')
    # with open('./cut.png', 'rb') as f:
    #     image = f.read()
    # sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
    # text = sdk.predict(image_bytes=image)
    cv.imread(r'./img/cut.png')


if __name__ == '__main__':
    main()
