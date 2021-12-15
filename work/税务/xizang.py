#encoding=utf-8

#税务违法   西藏信息获取

import requests
from selenium import webdriver
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
    options.add_argument('--headless')  # 无界面形式
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

    driver = webdriver.Chrome(executable_path='F:\chromedriver.exe')
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

def getInfo(i):
    url='https://xizang.chinatax.gov.cn/col/col2371/index.html'
    driver=getDriver()
    driver.get(url)
    #纳税人名称
    nsrmc='阿里地区双府家私商贸有限公司'
    #nsrmc='北京字节跳动科技有限公司'
    driver.find_element_by_xpath('//*[@id="searchTable"]/tbody/tr[1]/td[2]/input').send_keys(nsrmc)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="searchTable"]/tbody/tr[5]/td/input[8]').click()
    time.sleep(2)
    driver.switch_to.frame('showIframe')
    result=driver.find_element_by_xpath('/html/body/div/form/div/div/span').get_attribute('innerHTML')
    if re.findall(r"共&nbsp;0&nbsp;页&nbsp;到第",result):
        print('无符合公布标准的案件信息')
        driver.quit()
        exit(0)
    else:
        #print(re.sub(u"\\<.*?\\>","",result))
        driver.find_element_by_xpath('/html/body/div/table[2]/tbody/tr['+str(i)+']/td/table/tbody/tr/td[4]/a').click()
        all_h=driver.window_handles
        driver.switch_to.window(all_h[1])
        info=driver.find_element_by_xpath('//*[@id="zoom"]').get_attribute('innerHTML')
        #print(info)
        info="纳税人名称："+nsrmc+info
        info1=re.sub(u"\\</tr\\>",",",info)
        info2=re.sub(u"\\</td\\>", "、", info1)
        info3=re.sub(u"\\<.*?\\>","",info2)
        info4=re.sub(u"\n","",info3)
        info5=re.sub(u"\t","",info4)
        info6 = re.sub(u"begin-->", "", info5)
        info7 = re.sub(u"end-->", "", info6)
        info8 = info7.replace(' ', '').split(',')
        info9 = str(info8).replace("、'", "'").replace("、", ":")
        print(info9)
    driver.quit()
if __name__ == '__main__':
    try:
        for i in range(1,11):
            getInfo(i)
    except:
        exit(1)


'''
/html/body/div/table[2]/tbody/tr[2]/td/table/tbody/tr/td[4]/a
/html/body/div/table[2]/tbody/tr[1]/td/table/tbody/tr/td[4]/a
/html/body/div/table[2]/tbody/tr[8]/td/table/tbody/tr/td[4]/a
'''