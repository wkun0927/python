# encoding=utf-8


from selenium import webdriver
import requests
import time
import re


def getDriver():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4068.4 Safari/537.36'
    }
    url = 'http://17610040106.v4.dailiyun.com/query.txt?key=NP86444E99&word=&count=1&rand=false&ltime=0&norepeat=false&detail=false'
    response = requests.get(url, headers=headers)
    proxy_dly = response.text.strip()
    options = webdriver.ChromeOptions()
    if proxy_dly:
        proxies = {
            "http": "http://" + proxy_dly,
            "https": "http://" + proxy_dly
        }
        options.add_argument('--proxy-server' + proxies['https'])

    options.add_argument("--disable-extensions")  # 禁用扩展
    options.add_argument("--disable-gpu")  # 谷歌文档提到需要加上这个属性来规避bug
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # options.add_argument('--headless')  # 无界面形式
    options.add_argument('--no-sandbox')  # 取消沙盒模式
    # options.add_argument('-kiosk')    # 全屏
    # options.add_argument("--window-size=1920,900")  # 指定浏览器分辨率
    # options.set_window_size(480, 600)  # 窗口大小变化
    options.add_argument('--disable-setuid-sandbox')
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument('--incognito')  # 启动进入隐身模式
    options.add_argument('--lang=zh-CN')  # 设置语言为简体中文
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36')
    options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    options.add_argument('--disable-bundled-ppapi-flash')  # 禁用 Flash 的捆绑 PPAPI 版本
    options.add_argument('--mute-audio')  # 将发送到音频设备的音频静音，使其在自动测试期间听不到

    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })

    return driver


if __name__ == '__main__':
    url = "https://cprs.patentstar.com.cn/Account/LoginOut"
    driver = getDriver()
    driver.get(url)
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="loginname"]').send_keys('18410065868')
    driver.find_element_by_id('password').send_keys('2726kerwin')
    driver.find_element_by_xpath('//*[@id="login"]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="tablepage"]/a').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="TxtSearch"]').send_keys("((@华为技术有限公司/PA))*(1/PT+8/PT)*(1/LG)")
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="searchbtn2"]').click()
    time.sleep(3)
    pages = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[4]/div[2]/div[2]/a[3]').get_attribute(
        'innerHTML')
    print(pages)
    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[4]/div[2]/div[2]/a[4]').click()
    time.sleep(2)

    time.sleep(2)
    driver.quit()
