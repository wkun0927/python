# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-08-26 14:28:57
# @Description: 山西  滑动验证码 未完成


import base64
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from user_agent import generate_user_agent

from shanxi_yanzh import get


def getDriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--headless')  # 无界面形式
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
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"
    url = 'https://etax.shanxi.chinatax.gov.cn/gzfw/nsrzg'
    driver = getDriver()
    driver.get(url)
    WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//*[@id="NSR"]'))
    driver.find_element_by_xpath('//*[@id="NSR"]').send_keys(identifier)
    time.sleep(2)
    driver.find_element_by_xpath('//div[@class="search-form-column"]/button').click()

    while True:
        image_src_url = driver.find_element_by_xpath('//*[@id="captchaContainer"]/div/div/div[2]/div/div[1]/div/img').get_attribute('src').split(',', 1)[-1]
        img_data = base64.b64decode(image_src_url)
        with open('./0.jpg', 'wb') as f:
            f.write(img_data)
        dic = get()
        dic = eval(dic)
        x = dic['trace']
        element = driver.find_element_by_xpath('//div[@class="verify-move-block"]')
        action = ActionChains(driver)
        action.click_and_hold(element).perform()
        for step in x:
            action.move_by_offset(xoffset=step, yoffset=0).perform()
            action = ActionChains(driver)
        action.release().perform()
        time.sleep(2)
        try:
            info = driver.find_element_by_xpath('//*[@id="1"]').get_attribute('textContent')
            print(info)
            break
        except NoSuchElementException:
            continue
    driver.quit()


if __name__ == '__main__':
    ID = '911400001123599660'
    main(ID)
