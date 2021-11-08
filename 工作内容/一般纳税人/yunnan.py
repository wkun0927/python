# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-09-23 10:17:29
# @Descripttion: 云南省 数字验证码

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from user_agent import generate_user_agent
import time
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
    browser = webdriver.Chrome(options=options, executable_path='C:/Users/18410/AppData/Local/Google/Chrome/Application/chromedriver.exe')
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

    return browser


def main(identifier):
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"
    url = 'https://etax.yunnan.chinatax.gov.cn/zjgfdacx/sscx/ybnsrzgcx/ybnsrzgcx.html'
    driver = getDriver()
    driver.get(url)
    WebDriverWait(driver, 20).until(lambda x: x.find_element_by_xpath('//div[@class="text-left"]/input'))

    driver.find_element_by_xpath('//div[@class="text-left"]/input').send_keys(identifier)

    # 定位验证码在iframe中的坐标
    element = driver.find_element_by_xpath('//*[@id="codeImage"]')
    print(element.location)
    print(element.size)
    # 真实坐标需要加上iframe的坐标
    left = element.location['x'] + 284
    top = element.location['y'] + 39
    right = element.location['x'] + element.size['width'] + 305
    bottom = element.location['y'] + element.size['height'] + 46

    time.sleep(2)
    while True:
        # 截取验证码图片
        driver.save_screenshot('./验证码图片/yunnan_picture.png')  # 全屏截图

        im = Image.open('./验证码图片/yunnan_picture.png')
        im = im.crop((left, top, right, bottom))
        im.save('./验证码图片/yunnan_identifier.png')

        # 识别验证码
        with open('./验证码图片/yunnan_identifier.png', 'rb') as f:
            image = f.read()
        sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
        
        text = sdk.predict(image_bytes=image)
        print(text)
        # 输入验证码
        driver.find_element_by_xpath('//*[@id="check_code"]').send_keys(text)
        time.sleep(1)
        # 点击“查询”
        driver.find_element_by_xpath('//*[@id="queryBtn"]').click()
        time.sleep(3)
        try:
            count = 1
            while True:
                try:
                    info = driver.find_element_by_xpath('//*[@id="content"]/tr[' + str(count) + ']').get_attribute('textContent')
                    print(info)
                    count += 1
                except NoSuchElementException:
                    break
        except NoSuchElementException:
            mes = driver.find_element_by_xpath('//*[@id="content"]').get_attribute('textContent')
            if mes:
                driver.find_element_by_xpath('//*[contains(text(), "确定")]').click()
            driver.find_element_by_xpath('//*[@id="check_code"]').clear()  # 清除输入的验证码
            driver.find_element_by_xpath('//*[@id="codeImage"]').click()  # 点击刷新验证码
            time.sleep(2)
            continue

        break

    driver.quit()


if __name__ == '__main__':
    ID = '9153000021652214XX'
    main(ID)
