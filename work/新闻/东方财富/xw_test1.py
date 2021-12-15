# encoding=utf-8

import re
import requests
from selenium import webdriver


def getDriver():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4068.4 Safari/537.36'
    }
    url = 'http://17610040106.v4.dailiyun.com/query.txt?key=NP86444E99&word=&count=1&rand=false&ltime=0&norepeat=false&detail=false'
    response = requests.get(url, headers=headers)
    proxy_dly = response.text.strip()
    if proxy_dly:
        proxies = {
            "http": "http://" + proxy_dly,
            "https": "http://" + proxy_dly
        }
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")  # 禁用扩展
    options.add_argument("--disable-gpu")  # 谷歌文档提到需要加上这个属性来规避bug
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # options.add_argument('--headless')  # 无界面形式
    options.add_argument('--no-sandbox')  # 取消沙盒模式
    # options.add_argument('-kiosk')    # 全屏
    options.add_argument("--window-size=1920,900")  # 指定浏览器分辨率
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
    options.add_argument('--proxy-server' + proxies)
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


# 获取正文内容和图片
def get_text(url):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome()
    driver.get(url)
    # source = driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]').get_attribute('innerHTML')
    # source1 = re.sub(u"\\<.*?\\>", "", source)
    # source2 = re.sub(u" ", "", source1)
    # source3 = re.sub(u"\n*", "", source2)
    # print(source3)
    text_list = []
    try:  # 获取正文
        for i in range(1, 20):
            text = driver.find_element_by_xpath('//*[@id="ContentBody"]/p[' + str(i) + ']').get_attribute('innerHTML')
            text1 = re.sub(u"\\<.*?\\>", "", text)
            text2 = re.sub(u" ", "", text1)
            text3 = re.sub(u"\u3000", "", text2)
            text4 = re.sub(u"\n", "", text3)
            text5 = re.sub(u"&gt;", "", text4)
            text_list.append(text5)
    except:
        pass
    print(text_list)
    try:  # 获取图片
        for i in range(1, 10):
            pict = driver.find_element_by_xpath('//*[@id="ContentBody"]/center[' + str(i) + ']').get_attribute(
                'innerHTML')
            print(pict)
            src_pict = str(pict).split('"')[1]
            print(src_pict)
            name = src_pict.split('/')[-1]
            f = open(name + '.jpg', 'wb')
            response = requests.get(src_pict)
            f.write(response.content)
            f.close()

    except:
        pass
    driver.quit()


if __name__ == '__main__':
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome()
    url = 'https://so.eastmoney.com/web/s?keyword=字节跳动&pageindex=1'
    driver.get(url)
    for i in range(1, 3):  # 这页的i条新闻
        t1 = driver.find_element_by_xpath(
            '//*[@id="app"]/div[3]/div[1]/div[11]/div[1]/div[' + str(i) + ']/div[1]').get_attribute('innerHTML')
        # print(t1)
        link = re.findall(r"http:.*?html", t1)
        t1 = re.sub(u"\\<.*?\\>", '', t1)
        print(t1)
        print(link[0])
        get_text(link[0])
        print()

    driver.quit()

'''
//*[@id="app"]/div[3]/div[1]/div[11]/div[1]/div[1]/div[1]
//*[@id="app"]/div[3]/div[1]/div[11]/div[1]/div[2]/div[1]

'''
