# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021/8/30 下午5:24
# @LastEditors: 王琨
# @FileName: henan.py
# @Description: 河南

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
    options.add_argument('--user-agent=' + generate_user_agent())
    options.add_argument('--hide-scrollbars')
    options.add_argument('--disable-bundled-ppapi-flash')
    options.add_argument('--mute-audio')
    # options.add_argument('--proxy-server={}'.format(proxy(headers)))
    browser = webdriver.Chrome(options=options)
    browser.execute_cdp_cmd("Network.enable", {})
    browser.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {"source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
            })
        """})

    return browser


def main():
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"
    url = 'https://etax.henan.chinatax.gov.cn/web/dzswj/taxclient/ggfw/query/ybnsrcx.html'
    identifier = '91410300614820871W'
    driver = getDriver()
    driver.get(url)
    WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//*[@class="wxl_jnsrsbh"]'))

    driver.find_element_by_xpath('//*[@class="wxl_jnsrsbh"]').send_keys(identifier)

    time.sleep(2)
    while True:
        # 截取验证码图片
        driver.save_screenshot('./验证码图片/henan_picture.png')  # 全屏截图
        # 定位验证码在iframe中的坐标
        element = driver.find_element_by_id('picCode')
        print(element.location)
        print(element.size)
        # 真实坐标需要加上iframe的坐标
        left = element.location['x']
        top = element.location['y']
        right = element.location['x'] + element.size['width']
        bottom = element.location['y'] + element.size['height']
        im = Image.open('./验证码图片/henan_picture.png')
        im = im.crop((left, top, right, bottom))
        im.save('./验证码图片/henan_identifier.png')

        # 识别验证码
        with open('./验证码图片/henan_identifier.png', 'rb') as f:
            image = f.read()
        sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
        text = sdk.predict(image_bytes=image)
        print(text)
        # 输入验证码
        driver.find_element_by_xpath('//*[@name="rcode"]').send_keys(text)
        time.sleep(1)
        # 点击“查询”
        driver.find_element_by_xpath('//*[@class="wxl_btn wxl_bg_blue f_right"]').click()
        time.sleep(3)
        try:
            info = driver.find_element_by_xpath('//*[@class="odd"]').get_attribute('textContent')
        except NoSuchElementException:
            driver.find_element_by_xpath('//*[@name="rcode"]').clear()
            time.sleep(2)
            continue
        print(info)
        break

    driver.quit()


if __name__ == '__main__':
    main()
