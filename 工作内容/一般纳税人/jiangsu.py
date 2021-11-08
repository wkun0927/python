# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-09-01 16:32:21
# @Description: 江苏

import base64
import time

import pysnooper
import requests
from lxml import etree
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from user_agent import generate_user_agent

from jiangsu_yanzh import get
import pyautogui


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
        '--user-agent={}'.format(generate_user_agent()))
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
    # desired_capabilities = DesiredCapabilities.CHROME
    # desired_capabilities["pageLoadStrategy"] = "none"
    url = 'https://etax.jiangsu.chinatax.gov.cn/jx/commonquery/20181203/3440.html'
    driver = getDriver()
    driver.get(url)
    WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//*[@id="mainFrame"]'))
    # 获取iframe坐标
    ifr_ele = driver.find_element_by_xpath('//*[@id="mainFrame"]')
    ifr_x = ifr_ele.location['x']
    ifr_y = ifr_ele.location['y']
    # 进入iframe
    driver.switch_to.frame('mainFrame')
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="search_nsrsbh"]').send_keys(identifier)  # 输入识别号
    element = driver.find_element_by_xpath('//*[@id="captcha_div"]/div')
    ele_x = element.location['x'] + ifr_x
    ele_y = element.location['y'] + ifr_y
    for x in range(10):
        element.click()
        time.sleep(2)

        pic = driver.find_element_by_xpath('//*[@id="captcha_div"]/div/div[1]/div/div[1]/img[1]')
        pic_x = pic.location['x']
        pic_y = pic.location['y']
        pic_url = pic.get_attribute('src')
        res = requests.get(pic_url)
        with open('./验证码图片/jiangsu_identifier.jpg', 'wb') as f:
            f.write(res.content)
        dic = get()
        dic = eval(dic)
        character = driver.find_element_by_xpath('//*[@id="captcha_div"]/div/div[2]/div[3]/div/span').get_attribute('textContent')
        word = eval(character)
        element.click()
        img = driver.find_element_by_xpath('//img[@class="yidun_bg-img"]')
        # action = ActionChains(driver)
        for i in range(3):
            x = dic['data'][word[i]]['x'] + ifr_x + pic_x
            y = dic['data'][word[i]]['y'] + ifr_y + pic_y
            # action.move_to_element_with_offset(img, x, y).click()
            pyautogui.moveTo(x, y, duration=2, tween=pyautogui.easeInOutQuad)
            # action.perform()
            # action = ActionChains(driver)
            # time.sleep(1)
    time.sleep(1)
    driver.quit()


if __name__ == '__main__':
    ID = '9132070070404786XB'
    main(ID)
