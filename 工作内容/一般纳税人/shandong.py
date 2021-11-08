# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021/8/30 上午10:57
# @LastEditors: 王琨
# @FileName: shandong.py
# @Description: 山东 字母验证码


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
    browser = webdriver.Chrome(options=options)
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
    url = 'http://shandong.chinatax.gov.cn/col/col929/index.html#'
    identifier = '91370500267193796E'
    driver = getDriver()
    driver.get(url)
    # WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//*[@id="sscx_iframe"]'))
    time.sleep(5)
    # 获取iframe位置
    iframe_ele = driver.find_element_by_xpath('//*[@id="sscx_iframe"]')
    x = iframe_ele.location['x']
    y = iframe_ele.location['y']

    # iframe = driver.find_element_by_xpath('//*[@id="ifrMain"]')
    driver.switch_to.frame('sscx_iframe')
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="nsrsbh"]').send_keys(identifier)

    time.sleep(2)

    while True:
        # 截取验证码图片
        driver.save_screenshot('./验证码图片/qingdao_picture.png')  # 全屏截图
        # 定位验证码在iframe中的坐标
        element = driver.find_element_by_id('yanzm2')
        print(element.location)
        print(element.size)
        # 真实坐标需要加上iframe的坐标
        left = element.location['x'] + x
        top = element.location['y'] + y
        right = element.location['x'] + element.size['width'] + x
        bottom = element.location['y'] + element.size['height'] + y
        im = Image.open('./验证码图片/qingdao_picture.png')
        im = im.crop((left, top, right, bottom))
        im.save('./验证码图片/qingdao_identifier.png')

        # 识别验证码
        with open('./验证码图片/qingdao_identifier.png', 'rb') as f:
            image = f.read()
        sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
        text = sdk.predict(image_bytes=image)
        print(text)
        # 输入验证码
        driver.find_element_by_xpath('//*[@id="yzm2"]').send_keys(text)
        time.sleep(1)
        # 点击“查询”
        driver.find_element_by_xpath('//*[@id="form2"]//tr[3]//input[1]').click()
        time.sleep(3)
        try:
            info = driver.find_element_by_xpath('//*[@id="form2"]/table/tbody').get_attribute('textContent')
            print(info)
        except NoSuchElementException:
            driver.quit()
            main()
        break

    driver.quit()


if __name__ == '__main__':
    main()
