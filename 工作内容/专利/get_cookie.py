# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-10-20 13:43:29
# @Descripttion:

import json
import random
import re
import string
import time

import cv2 as cv
import muggle_ocr
import pysnooper
import pytesseract
import requests
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
    # options.add_argument('--proxy-server={}'.format(get_proxies()))
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


def recognize_text(image):
    # 打开文件夹中的图片
    image = Image.open('./img/cut.png')
    # 灰度图
    lim = image.convert('L')
    # 灰度阈值设为165，低于这个值的点全部填白色
    threshold = 150
    table = []

    for j in range(256):
        if j < threshold:
            table.append(0)
        else:
            table.append(1)

    bim = lim.point(table, '1')
    bim.save('./img/cut.png')
    text = pytesseract.image_to_string(bim)
    text = re.findall('\d+', text)
    text = ''.join(text)
    print(text)
    return text


def main():
    List = []
    info = dict()
    url = 'http://123.233.113.66:8060//pubsearch/portal/uilogin-forwardLogin.shtml'
    with open('./data/总网站.json') as f:
        userinfo = json.load(f)

    for username in userinfo.keys():
        password = userinfo[username]
        driver = getDriver()
        driver.get(url)
        WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, '//*[@id="j_username"]'))
        while True:
            name = driver.find_element(By.XPATH, '//*[@id="j_username"]')
            name.click()
            time.sleep(1)
            name.send_keys(username)  # 输入用户名
            word = driver.find_element(By.XPATH, '//*[@id="j_password_show"]')
            word.click()
            time.sleep(1)
            word.send_keys(password)  # 输入用户密码

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
            src = cv.imread(r'./img/cut.png')
            text = recognize_text(src)
            driver.find_element(By.XPATH, '//*[@id="j_validation_code"]').send_keys(text)  # 输入密码
            driver.find_element(By.XPATH, '//*[@id="loginForm"]/div[5]/a').click()  # 点击登陆
            time.sleep(5)
            try:
                # 是否有输入错误，有则重新开始，无则跳过。
                driver.find_element(By.XPATH, '//*[@i="button"]').click()
                driver.find_element(By.XPATH, '//*[@id="j_username"]').clear()
                driver.find_element(By.XPATH, '//*[@id="j_password_show"]').clear()
                driver.find_element(By.XPATH, '//*[@id="codePic"]').click()
                time.sleep(2)
                continue
            except Exception as e:
                print(e)
                break
        try:
            info = driver.find_element(By.XPATH, '//div/div/div/div[1]/div/p/span')
            if info == '您当前访问的用户名已被屏蔽，请联系管理员。':
                del userinfo[username]
                continue
        except Exception:
            pass
        cookies = driver.get_cookies()
        JSESSIONID = cookies[-1]['value']
        List.append(JSESSIONID)
        time.sleep(1)
        driver.quit()
    info['http://123.233.113.66:8060/'] = List
    with open('./data/cookie.json', 'w') as s:
        json.dump(info, s)

    with open('./data/总网站.json', 'w') as j:
        f.write(userinfo, j)


if __name__ == '__main__':
    main()
