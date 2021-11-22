#encoding=utf-8

#税务违法   宁波市信息获取

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
    # options.add_argument('--headless')  # 无界面形式
    # options.add_argument('--no-sandbox')  # 取消沙盒模式
    # options.add_argument('-kiosk')    # 全屏

    # options.set_window_size(480, 600)  # 窗口大小变化
    options.add_argument('--incognito')  # 启动进入隐身模式
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36')
    # options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    # options.add_argument('--disable-bundled-ppapi-flash')  # 禁用 Flash 的捆绑 PPAPI 版本
    # options.add_argument('--mute-audio')  # 将发送到音频设备的音频静音，使其在自动测试期间听不到

    driver = webdriver.Chrome(executable_path='F:\chromedriver.exe', options=options)
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
    url='http://ningbo.chinatax.gov.cn/col/col6166/index.html'
    driver=getDriver()
    driver.get(url)
    time.sleep(2)

    frame = driver.find_element_by_xpath('//*[@id="barrierfree_container"]/div[3]/div/table/tbody/tr/td[5]/div[1]/iframe')
    driver.switch_to.frame(frame)
    #纳税人名称
    nsrmc='宁波市鄞州杰辉服装辅料有限公司'
    #nsrmc='北京字节跳动科技有限公司'
    driver.find_element_by_xpath('//*[@id="q"]').send_keys(nsrmc)
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/form/table[1]/tbody/tr[5]/td[2]/input').click()
    time.sleep(2)

    result=driver.find_element_by_xpath('//*[@id="search-form"]/div[2]/div[6]/div[2]/div/div/div/div[2]').get_attribute('innerHTML')
    if not re.findall(r"详细信息",result):
        print('无符合公布标准的案件信息')
    else:
        time.sleep(5)
        #print(re.sub(u"\\<.*?\\>","",result))
        driver.find_element_by_xpath('//*[@id="search-form"]/div[2]/div[6]/div[2]/div/div/div/div[2]/table/tbody/tr/td[5]/a').click()
        all_h=driver.window_handles
        driver.switch_to.window(all_h[1])
        info=driver.find_element_by_xpath('//*[@id="zoom"]/table/tbody').get_attribute('innerHTML')
        #print(info)
        info1=re.sub(u"\\</tr\\>",",",info)
        info2=re.sub(u"\\</td\\>", "、", info1)
        info3=re.sub(u"\\<.*?\\>","",info2)
        info4=re.sub(u"\n","",info3)
        info5=re.sub(u"\t","",info4)
        info6=info5.replace(' ','').split(',')
        print(info6)

    driver.quit()


'''
//*[@id="search-form"]/div[2]/div[6]/div[2]/div/div/div/div[2]/table/tbody/tr/td[5]/a
//*[@id="search-form"]/div[2]/div[6]/div[2]/div/div/div/div[2]/table[1]/tbody/tr/td[5]/a
//*[@id="search-form"]/div[2]/div[6]/div[2]/div/div/div/div[2]/table[2]/tbody/tr/td[5]/a
'''