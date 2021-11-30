#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-10-20 13:43:29
# @Descripttion:

import json
import re
import time

import cv2 as cv
import pytesseract
import redis
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
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
    browser.set_window_size(1920, 1080)
    browser.execute_cdp_cmd("Network.enable", {})
    browser.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {"source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
            })
        """})

    return browser


def recognize_text(image, img_path):
    # 打开文件夹中的图片
    image = Image.open(img_path)
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
    bim.save(img_path)
    text = pytesseract.image_to_string(bim)
    text = re.findall('\d+', text)
    text = ''.join(text)
    print(text)
    return text


def main():
    cookie = dict()
    img_full_path = '/home/wkun/Dev/python/work/patent/img/full.png'
    img_cut_path = '/home/wkun/Dev/python/work/patent/img/cut.png'
    url = 'http://60.166.52.165:8030/pubsearch/portal/uilogin-forwardLogin.shtml'
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    pairs = r.hgetall('account_group2')
    userinfo = dict()
    for key, value in pairs.items():
        key = str(key, encoding="utf-8")
        value = str(value, encoding="utf-8")
        userinfo[key] = value

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
            driver.save_screenshot(img_full_path)
            left = img.location['x']
            top = img.location['y']
            right = img.location['x'] + img.size['width']
            bottom = img.location['y'] + img.size['height']
            im = Image.open(img_full_path)
            im = im.crop((left, top, right, bottom))
            im.save(img_cut_path)
            src = cv.imread(img_cut_path)
            text = recognize_text(src, img_cut_path)
            driver.find_element(By.XPATH, '//*[@id="j_validation_code"]').send_keys(text)  # 输入验证码
            driver.find_element(By.XPATH, '//*[@id="loginForm"]/div[5]/a').click()  # 点击登陆
            time.sleep(1)
            try:
                # 是否有输入错误，有则重新开始，无则跳过。
                mes = driver.find_element(By.XPATH, '//*[@i="content"]').get_attribute('textContent')
                if mes == '验证码错误！Verification Code Error!':
                    driver.find_element(By.XPATH, '//*[@type="button"]').click()
                    driver.find_element(By.XPATH, '//*[@id="j_username"]').clear()
                    driver.find_element(By.XPATH, '//*[@id="j_password_show"]').clear()
                    driver.find_element(By.XPATH, '//*[@id="j_validation_code"]').clear()
                    driver.find_element(By.XPATH, '//*[@id="codePic"]').click()
                    continue
                elif mes == '登录失败次数超过6次，帐号锁定，30分钟内不能登录':
                    n = 1
                    break
                elif mes == '用户名或密码错误！ Username or password error!':
                    n = 2
                    break
            except NoSuchElementException:
                n = 0
                break
            except Exception as e:
                n = 0
                print(e)
                break

        if n == 1:
            continue
        elif n == 2:
            r.hdel('account_group1', username)
            driver.quit()
            continue
        time.sleep(5)
        try:
            pingbi = driver.find_element(By.XPATH, '//div/div/div/div[1]/div/p/span').get_attribute('textContent')
            if pingbi == '您当前访问的用户名已被屏蔽，请联系管理员。':
                r.hdel('account_group1', username)
                continue
        except Exception:
            pass
        cookies = driver.get_cookies()
        JSESSIONID = cookies[-1]['value']
        cookie['username'] = JSESSIONID
        time.sleep(1)
        driver.quit()
        r.lpush('cookie_group2', JSESSIONID)
    # info['JSESSIONID'] = cookie
    # r.hset('cookie_group1', mapping=cookie)
    # with open(cookie_path, 'w') as s:
    #     json.dump(info, s)


if __name__ == '__main__':
    main()
