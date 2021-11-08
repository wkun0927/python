# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021/8/30 下午5:40
# @LastEditors: 王琨
# @FileName: hubei.py
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
from PIL import Image


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


def main(identifier):
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"
    url = 'https://etax.hubei.chinatax.gov.cn/portal/iframe.c?dm=undefined&menu=GZFW_00&title=%E4%B8%80%E8%88%AC%E7%BA%B3%E7%A8%8E%E4%BA%BA%E8%B5%84%E6%A0%BC%E6%9F%A5%E8%AF%A2&wtfk_menu=170000305&goUrl=/zyy-typt/views/dzswj/typt/ggcx/sfybnsr.jsp'
    driver = getDriver()
    driver.get(url)
    WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id('ifm'))

    time.sleep(1)

    # 获取iframe位置
    iframe_ele = driver.find_element_by_id('ifm')
    x = iframe_ele.location['x']
    y = iframe_ele.location['y']

    driver.switch_to.frame('ifm')
    # WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//*[@id="nsrsbhmc"]'))
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="nsrsbh"]').send_keys(identifier)

    time.sleep(2)

    while True:
        # 截取验证码图片
        driver.save_screenshot('./验证码图片/hubei_picture.png')  # 全屏截图
        # 定位验证码在iframe中的坐标
        element = driver.find_element_by_id('imgObj')
        print(element.location)
        print(element.size)
        # 真实坐标需要加上iframe的坐标
        left = element.location['x'] + x
        top = element.location['y'] + y
        right = element.location['x'] + element.size['width'] + x
        bottom = element.location['y'] + element.size['height'] + y
        im = Image.open('./验证码图片/hubei_picture.png')
        im = im.crop((left, top, right, bottom)).convert('RGB')
        width = im.size[0]
        height = im.size[1]
        for x in range(0, width):
            for y in range(0, height):
                data = im.getpixel((x, y))
                print(data)
                if data[0] <= 30 and data[1] <= 30 and data[2] <= 30:
                    im.putpixel((x, y), (255, 255, 255))
        img = im.convert('RGB')

        img.save('./验证码图片/hubei_identifier.png')

        # 识别验证码
        with open('./验证码图片/hubei_identifier.png', 'rb') as f:
            image = f.read()
        sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
        text = sdk.predict(image_bytes=image)
        print(text)
        driver.find_element_by_xpath('//*[@name="code"]').send_keys(text)
        time.sleep(1)
        driver.find_element_by_xpath('//input[@value="查询 "]').click()
        time.sleep(3)
        try:
            info = driver.find_element_by_xpath('//*[@id="table2"]/thead/tr[2]').get_attribute('textContent')
        except NoSuchElementException:
            info = driver.find_element_by_xpath('//div[2]/div[2]/div[2]').get_attribute('textContent')
            if info == '验证码错误！':
                driver.find_element_by_xpath('//span[contains(text(),"确定")]').click()
                driver.find_element_by_xpath('//*[@name="code"]').clear()
                continue
            elif info == '未查询到相关数据':
                print('请重新输入纳税人识别号！')
        print(info)
        break

    driver.quit()


if __name__ == '__main__':
    ID = '914200001776002711'
    main(ID)
    next_bookmark
