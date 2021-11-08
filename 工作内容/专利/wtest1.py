# encoding=utf-8
# 最多可访问200页 即1000条记录
# 可通过分类缩小范围以获取更多的数据      改变检索式就行

import re
import time

import requests
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait


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

    driver = webdriver.Chrome(options=options, executable_path='C:/Program Files/Google/Chrome/Application/chromedriver.exe')
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
    # desired_capabilities = DesiredCapabilities.CHROME
    # desired_capabilities["pageLoadStrategy"] = "none"
    driver = getDriver()
    driver.get(url)
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="loginname"]').send_keys('18410065868')  # 登录页  需要账号密码
    driver.find_element_by_id('password').send_keys('2726kerwin')
    driver.find_element_by_xpath('//*[@id="login"]').click()
    time.sleep(2)
    import ipdb
    ipdb.set_trace()
    driver.find_element_by_xpath('//*[@id="tablepage"]/a').click()
    time.sleep(1)
    '''
    根据情况写表达式
    @华为技术有限公司   F XX (@华为技术有限公司/PA)
    发明+有效        ((@华为技术有限公司/PA))*(1/PT+8/PT)*(1/LG)
    发明+审中        ((@华为技术有限公司/PA))*(1/PT+8/PT)*(3/LG)
    发明+失效        ((@华为技术有限公司/PA))*(1/PT+8/PT)*(2/LG)
    实用新型+有效     ((@华为技术有限公司/PA))*(2/PT+9/PT)*(1/LG)
    实用新型+审中     ((@华为技术有限公司/PA))*(2/PT+9/PT)*(3/LG)
    实用新型+失效     ((@华为技术有限公司/PA))*(2/PT+9/PT)*(2/LG)
    外观+有效        ((@华为技术有限公司/PA))*(3/PT)*(1/LG)
    外观+审中        ((@华为技术有限公司/PA))*(3/PT)*(3/LG)
    外观+失效        ((@华为技术有限公司/PA))*(3/PT)*(2/LG)
    '''
    driver.find_element_by_xpath('//*[@id="TxtSearch"]').send_keys("((@华为技术有限公司/PA))*(1/PT+8/PT)*(1/LG)")
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="searchbtn2"]').click()
    time.sleep(3)
    flag = 0
    pages = 0
    while True:
        for i in range(1, 6):
            try:
                # WebDriverWait(driver, 100).until(lambda first: first.find_element_by_xpath('//*[@id="listcontainer"]/div['+str(i)+']'))
                info = driver.find_element_by_xpath('//*[@id="listcontainer"]/div[' + str(i) + ']').get_attribute(
                    'innerHTML').replace('\u2011', '')
            except Exception as e:
                driver.quit()
                print(e)
                exit(0)
            info1 = re.sub(u"</div>", "*", info)
            info1 = re.sub(u"</p>", ",", info1)
            info2 = re.sub(u"<.*?>", " ", info1)
            info3 = re.sub(u"\n", "", info2)
            info4 = re.sub(u"\t", "", info3)
            info5 = re.sub(u" ", "", info4)
            info6 = re.sub(u"&nbsp", "", info5)
            info7 = re.sub(u"\*", "\n", info6)
            info8 = re.sub(u";;收藏;;导出", "", info7)
            print(info8)
        flag = flag + 1
        try:

            if flag == 1:
                # WebDriverWait(driver, 100).until(lambda first: first.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[4]/div[2]/div[2]/a[4]'))
                pages = driver.find_element_by_xpath(
                    '/html/body/div[1]/div[2]/div/div[2]/div[4]/div[2]/div[2]/a[3]').get_attribute('innerHTML')
                driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[4]/div[2]/div[2]/a[4]').click()
                continue
            elif flag == 2 or flag == int(pages) - 1:
                # 倒数第二页会变为a[5]
                # WebDriverWait(driver, 100).until(lambda first: first.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[4]/div[2]/div[2]/a[5]'))
                driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[4]/div[2]/div[2]/a[5]').click()
                # continue
                break
            elif flag == int(pages):
                # 最后一页不能点，直接退出
                break
            else:
                # WebDriverWait(driver, 100).until(lambda first: first.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[4]/div[2]/div[2]/a[6]'))
                driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[4]/div[2]/div[2]/a[6]').click()
                continue
        except:
            break
    driver.quit()
