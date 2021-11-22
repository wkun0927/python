'''
自己在线预测准确性
滑动验证码分为两个模式：
第一个模式有滑块和缺口图，此时使用slide_block_distance函数获取滑动距离。
第二个模式是含有背景图和缺口原图，此时使用slide_noblock_distance获取滑动距离。
最后使用GTrace获取滑动轨迹
'''

import cv2
from call import main
from selenium import webdriver
import time
import numpy as np
from selenium.webdriver.common.action_chains import ActionChains
from urllib3.exceptions import LocationParseError
from requests.exceptions import ProxyError
import random


def getDriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")  # 禁用扩展
    options.add_argument("--disable-gpu")  # 谷歌文档提到需要加上这个属性来规避bug
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # options.add_argument('--headless')  # 无界面形式
    options.add_argument('--no-sandbox')  # 取消沙盒模式
    options.add_argument('--disable-setuid-sandbox')
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument('--incognito')  # 启动进入隐身模式
    options.add_argument('--lang=zh-CN')  # 设置语言为简体中文
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36')
    options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    options.add_argument('--disable-bundled-ppapi-flash')  # 禁用 Flash 的捆绑 PPAPI 版本
    options.add_argument('--mute-audio')  # 将发送到音频设备的音频静音，使其在自动测试期间听不到

    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """})
    return driver


def isElementExist(error_element):
    flag = True
    try:
        driver.find_element_by_xpath(error_element)
        return flag
    except:
        flag = False
        return flag


if __name__ == '__main__':
    import base64
    url = "https://etax.shanxi.chinatax.gov.cn/gzfw/nsrzg"
    driver = getDriver()
    driver.get(url)
    time.sleep(1)
    num_id = 0
    driver.find_element_by_xpath('//*[@id="NSR_MC"]').send_keys('百度')
    # 点击查询按钮
    driver.find_element_by_xpath('//*[@id="searchForm"]/div/div[1]/div[3]/button').click()
    time.sleep(random.randint(2, 4))
    # 点击按钮进行验证
    try:
        # 获得图片
        image_arc_url = driver.find_element_by_xpath('//*[@id="captchaContainer"]/div/div/div[2]/div/div[1]/div/img').get_attribute('src').split(',', 1)[1]
        img_data = base64.b64decode(image_arc_url)
        nparr = np.fromstring(img_data, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # slider_q=requests.get(image_arc_url).content#带有缺口的图片
        # 获得距离和滑动轨迹
        distance, x = main(img_np)
        # 获取拖动按钮
        buttun = driver.find_element_by_xpath('//*[@id="captchaContainer"]/div/div/div[2]/div/div[2]/div/div')
        action = ActionChains(driver)
        # 按住滑块不放
        action.click_and_hold(buttun).perform()
        # 根据轨迹执行滑动动作
        for step in x:
            # step偏移
            action.move_by_offset(xoffset=step, yoffset=0).perform()
            action = ActionChains(driver)
        action.release().perform()
        time.sleep(random.randint(1, 3))
    except LocationParseError:
        print(1)
    except ProxyError:
        print(2)

    driver.quit()
