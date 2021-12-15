# -*- coding: utf-8 -*-
# @Author              : wangkun
# @Date                : 2021-07-09 11:31:19
# @LastEditTime        : 2021-07-22 18:27:02
# @LastEditors         : 王琨
# @FilePath            : \pythonProject\Trademark_test.py
# @Description         : 商标网 selenium+pyautgui

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from user_agent import generate_user_agent
import pyautogui
import ipdb
import requests
import time
import random


def proxy(headers):
    while True:
        proxy_url = 'http://17610040106.v4.dailiyun.com/query.txt?key=NP86444E99&word=&count=1&rand=false&ltime=0&norepeat=false&detail=false'
        response = requests.get(proxy_url, headers=headers)
        proxies = response.text.strip()
        if proxies:
            break
        else:
            time.sleep(20)
    print(proxies)
    return proxies


def getDriver(headers):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument('--disable-blink-features=AutomationControlled')
    # options.add_argument('--headless')  # 无界面形式
    options.add_argument('--no-sandbox')  # 取消沙盒模式
    options.add_argument('--disable-setuid-sandbox')
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--incognito')  # 启动进入隐身模式
    options.add_argument('--lang=zh-CN')  # 设置语言为简体中文
    options.add_argument(
        '--user-agent=' + generate_user_agent())
    options.add_argument('--hide-scrollbars')
    options.add_argument('--disable-bundled-ppapi-flash')
    options.add_argument('--mute-audio')
    options.add_argument('--proxy-server={}'.format(proxy(headers)))
    browser = webdriver.Chrome(options=options,
                               executable_path='C:/Users/18410/AppData/Local/Google/Chrome/Application/chromedriver.exe')
    browser.execute_cdp_cmd("Network.enable", {})
    browser.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    with open('stealth.min.js') as f:
        js = f.read()
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
    })
    browser.implicitly_wait(10)

    return browser


url = 'http://sbj.cnipa.gov.cn/'
headers = {
    "User-Agent": generate_user_agent()
}
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["pageLoadStrategy"] = "none"
driver = getDriver(headers)
driver.maximize_window()
driver.get(url)

WebDriverWait(driver, 10).until(lambda element: element.find_element_by_xpath('//*[@class="bscont2 bscont"]//a'))
pyautogui.PAUSE = 1
pyautogui.moveTo(606, 1034, duration=1, tween=pyautogui.easeInOutQuad)
pyautogui.click()

handles = driver.window_handles
driver.switch_to.window(handles[-1])
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="TRS_Editor"]')))
pyautogui.moveTo(978, 829, duration=2, tween=pyautogui.easeInOutQuad)
pyautogui.click()

WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//p[contains(text(),"商标综合查询")]')))
pyautogui.moveTo(859, 521, duration=2, tween=pyautogui.easeInOutQuad)
pyautogui.click()


handles = driver.window_handles
driver.switch_to.window(handles[-1])

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="submitForm"]//tbody/tr[4]//input')))
pyautogui.moveTo(832, 610, duration=2, tween=pyautogui.easeInOutQuad)
pyautogui.click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="submitForm"]//tbody/tr[4]//input').send_keys('华为技术有限公司')
pyautogui.moveTo(931, 791, duration=1, tween=pyautogui.easeInOutQuad)
pyautogui.click()
ipdb.set_trace()
handles = driver.window_handles
driver.switch_to.window(handles[-1])
while True:
    for i in range(1, 51):
        img = driver.find_element_by_xpath('//tr[@class="ng-scope"][' + str(i) + ']/td/input').get_attribute('img')
        content = driver.find_element_by_xpath('//tr[@class="ng-scope"][' + str(i) + ']').get_attribute('textContent')
        print(img, content)
    try:
        driver.find_element_by_xpath('//*[@class="pagination pagination-right"]//li[@class="nextPage"]/a').click()
    except Exception:
        break
    time.sleep(random.randint(0, 5))
