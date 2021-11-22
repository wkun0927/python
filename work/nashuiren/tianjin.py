# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-08-26 10:59:39
# @LastEditors: 王琨
# @LastEditTime: 2021-08-26 11:03:41
# @FilePath: /python/工作内容/一般纳税人/tianjin.py
# @Description: 天津一般纳税人查询

import time

import muggle_ocr
from PIL import Image
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
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
    browser = webdriver.Chrome(options=options, executable_path='C:/Users/18410/AppData/Local/Google/Chrome/Application/chromedriver.exe')
    browser.maximize_window()
    browser.execute_cdp_cmd("Network.enable", {})
    browser.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {"source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
            })
        """})
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
    url = 'http://tianjin.chinatax.gov.cn/wzcx/ssxxggCx.action?gglx=11'
    taxpayer_name = '狗不理'
    driver = getDriver()
    driver.get(url)
    # WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//div[contains(text(),"一般纳税人资格查询")]'))
    time.sleep(2)
    driver.find_element_by_xpath('//div[contains(text(),"一般纳税人资格查询")]').click()
    time.sleep(1)
    iframe = driver.find_element_by_xpath('//div[2]/div/div/div[2]/iframe')

    iframe_ele = driver.find_element_by_xpath('//div[2]/div/div/div[2]/iframe')
    x = iframe_ele.location['x']
    y = iframe_ele.location['y']

    driver.switch_to.frame(iframe)
    driver.find_element_by_id('nsrmc').send_keys(taxpayer_name)

    # 截取验证码图片
    driver.save_screenshot('./验证码图片/tianjin_picture.png')  # 全屏截图
    # 定位验证码在iframe中的坐标
    element = driver.find_element_by_id('code')
    print(element.location)
    print(element.size)
    # 真实坐标需要加上iframe的坐标
    left = element.location['x'] + x
    top = element.location['y'] + y
    right = element.location['x'] + element.size['width'] + x
    bottom = element.location['y'] + element.size['height'] + y
    im = Image.open('./验证码图片/tianjin_picture.png')
    im = im.crop((left, top, right, bottom))
    im.save('./验证码图片/tianjin_identifier.png')

    # 识别验证码
    with open('./验证码图片/tianjin_identifier.png', 'rb') as f:
        image = f.read()
    sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
    text = sdk.predict(image_bytes=image)
    print(text)
    driver.find_element_by_id('jym').send_keys(text)
    time.sleep(1)
    driver.find_element_by_id('button').click()
    time.sleep(3)

    for i in range(1, 21):
        info = driver.find_element_by_xpath('//td[@class="tdb"]//tbody[2]/tr[' + str(i) + ']').get_attribute('textContent')
        print(info)
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


if __name__ == '__main__':
    main()
