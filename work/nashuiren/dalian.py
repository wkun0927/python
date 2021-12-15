# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-08-26 15:32:20
# @Description: 大连 数字识别验证码

import time

import muggle_ocr
from PIL import Image
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
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
    url = 'https://etax.dalian.chinatax.gov.cn/portal?target=gzfw'
    identifier = '91210213744367948'
    driver = getDriver()
    driver.get(url)
    WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id('neverGuide'))
    driver.find_element_by_xpath('//*[@id="neverGuide"]').click()
    driver.find_element_by_xpath('//*[@id="gzcxMenu"]/li[11]/a').click()
    time.sleep(1)

    # 获取iframe位置
    iframe_ele = driver.find_element_by_xpath('//*[@id="layui-layer8"]/div[2]')
    x = iframe_ele.location['x']
    y = iframe_ele.location['y']

    iframe = driver.find_element_by_xpath('//div[4]/div[2]/iframe')
    driver.switch_to.frame(iframe)
    # WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//*[@id="nsrsbhmc"]'))
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="nsrsbhmc"]').send_keys(identifier)

    time.sleep(2)

    while True:
        # 截取验证码图片
        driver.save_screenshot('./验证码图片/dalian_picture.png')  # 全屏截图
        # 定位验证码在iframe中的坐标
        element = driver.find_element_by_id('imgYzm')
        print(element.location)
        print(element.size)
        # 真实坐标需要加上iframe的坐标
        left = element.location['x'] + x
        top = element.location['y'] + y
        right = element.location['x'] + element.size['width'] + x
        bottom = element.location['y'] + element.size['height'] + y
        im = Image.open('./验证码图片/dalian_picture.png')
        im = im.crop((left, top, right, bottom))
        im.save('./验证码图片/dalian_identifier.png')

        # 识别验证码
        with open('./验证码图片/dalian_identifier.png', 'rb') as f:
            image = f.read()
        sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
        text = sdk.predict(image_bytes=image)
        print(text)
        driver.find_element_by_xpath('//*[@id="yzm"]').send_keys(text)
        time.sleep(1)
        driver.find_element_by_xpath('//button[contains(text(),"查询")]').click()
        time.sleep(3)

        info = driver.find_element_by_xpath('//*[@id="dataTable"]/tbody/tr').get_attribute('textContent')
        if info == '没有找到匹配的记录':
            driver.find_element_by_xpath('//a[contains(text(),"确定")]').click()
            driver.find_element_by_xpath('//*[@id="yzm"]').clear()
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


if __name__ == "__main__":
    main()
