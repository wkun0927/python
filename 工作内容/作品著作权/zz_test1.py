# encoding=utf-8

from selenium import webdriver
from selenium.webdriver.support.select import Select
import re
import time
import requests


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

    driver = webdriver.Chrome(executable_path='C:/Users/18410/AppData/Local/Google/Chrome/Application/chromedriver.exe', options=options)
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


def getProxy():
    while True:
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
            return proxies
        else:
            time.sleep(20)


if __name__ == '__main__':
    url = "http://qgzpdj.ccopyright.com.cn/registrationPublicity.html"
    driver = getDriver()
    driver.get(url)
    time.sleep(1)
    # 下拉框
    select = driver.find_element_by_xpath('//*[@id="searchType"]')
    Select(select).select_by_value('2')
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="searchCont"]').send_keys('华为技术有限公司')
    driver.find_element_by_xpath('//*[@id="j-popup"]').click()
    time.sleep(30)
    while True:
        # 得到每一栏的著作信息
        for i in range(1, 11):
            try:
                texts = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div/div/table[' + str(i) + ']/tbody').get_attribute('innerHTML')
                texts1 = re.sub(u'</tr>', ',', texts)
                texts2 = re.sub(u'<.*?>', '', texts1)
                print(texts2)
            except Exception as e:
                print(e)
                driver.quit()
                exit(0)
        time.sleep(3)
        try:
            driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div/div/div/div/button[2]/i').click()
        except:
            print(2)
            driver.quit()
            exit(0)
        time.sleep(20)

'''

作品/制品, 作品名称：趣味变妆-圣诞特辑 著作权人/权利人：华为技术有限公司, 作品类别：其他 登记机构：, 登记号：国作登字-2021-L-00027777 登记日期：2021-02-04, 创作完成日期：2020-12-15 首次发表日期：2020-12-23,   
作品/制品, 作品名称：趣味变妆-一期素材 著作权人/权利人：华为技术有限公司, 作品类别：其他 登记机构：, 登记号：国作登字-2021-L-00027776 登记日期：2021-02-04, 创作完成日期：2020-12-15 首次发表日期：2020-12-23,   
作品/制品, 作品名称：3D CuteMoji-013_dinosaur 著作权人/权利人：华为技术有限公司, 作品类别：美术 登记机构：, 登记号：国作登字-2021-F-00025677 登记日期：2021-02-03, 创作完成日期：2020-10-15 首次发表日期：,   
作品/制品, 作品名称：3D CuteMoji-008_bear 著作权人/权利人：华为技术有限公司, 作品类别：美术 登记机构：, 登记号：国作登字-2021-F-00025676 登记日期：2021-02-03, 创作完成日期：2020-07-15 首次发表日期：2020-08-15,   
作品/制品, 作品名称：3D CuteMoji-016_cattledad 著作权人/权利人：华为技术有限公司, 作品类别：美术 登记机构：, 登记号：国作登字-2021-F-00025675 登记日期：2021-02-03, 创作完成日期：2020-12-15 首次发表日期：,   
作品/制品, 作品名称：3D CuteMoji-018_raccoon 著作权人/权利人：华为技术有限公司, 作品类别：美术 登记机构：, 登记号：国作登字-2021-F-00025674 登记日期：2021-02-03, 创作完成日期：2021-01-05 首次发表日期：,   
作品/制品, 作品名称：3D CuteMoji-015_dog 著作权人/权利人：华为技术有限公司, 作品类别：美术 登记机构：, 登记号：国作登字-2021-F-00025673 登记日期：2021-02-03, 创作完成日期：2020-11-30 首次发表日期：,   
作品/制品, 作品名称：3D CuteMoji-006_fox 著作权人/权利人：华为技术有限公司, 作品类别：美术 登记机构：, 登记号：国作登字-2021-F-00025672 登记日期：2021-02-03, 创作完成日期：2020-07-30 首次发表日期：2020-08-15,   
作品/制品, 作品名称：3D CuteMoji-009_mouse 著作权人/权利人：华为技术有限公司, 作品类别：美术 登记机构：, 登记号：国作登字-2021-F-00025671 登记日期：2021-02-03, 创作完成日期：2020-08-30 首次发表日期：2020-12-15,   
作品/制品, 作品名称：3D CuteMoji-011_tiger 著作权人/权利人：华为技术有限公司, 作品类别：美术 登记机构：, 登记号：国作登字-2021-F-00025670 登记日期：2021-02-03, 创作完成日期：2020-09-15 首次发表日期：2020-12-15,   
作品/制品, 作品名称：3D CuteMoji-001_lion 著作权人/权利人：华为技术有限公司, 作品类别：美术 登记机构：, 登记号：国作登字-2021-F-00025669 登记日期：2021-02-03, 创作完成日期：2020-04-30 首次发表日期：2020-07-14,   
作品/制品, 作品名称：3D CuteMoji-014_babecattle 著作权人/权利人：华为技术有限公司, 作品类别：美术 登记机构：, 登记号：国作登字-2021-F-00024143 登记日期：2021-02-02, 创作完成日期：2020-11-15 首次发表日期：,   
作品/制品, 作品名称：3D CuteMoji-017_cattlemom 著作权人/权利人：华为技术有限公司, 作品类别：美术 登记机构：, 登记号：国作登字-2021-F-00024142 登记日期：2021-02-02, 创作完成日期：2020-01-05 首次发表日期：,   
作品/制品, 作品名称：3D CuteMoji-010_owl 著作权人/权利人：华为技术有限公司, 作品类别：美术 登记机构：, 登记号：国作登字-2021-F-00024141 登记日期：2021-02-02, 创作完成日期：2020-09-30 首次发表日期：2020-12-15,   
作品/制品, 作品名称：华为全连接开放实验室 LOGO 著作权人/权利人：华为技术有限公司, 作品类别：美术 登记机构：, 登记号：国作登字-2020-F-00973504 登记日期：2020-01-17, 创作完成日期：2019-12-24 首次发表日期：,   
作品/制品, 作品名称：华为全连接开放实验室1+8+N图标 著作权人/权利人：华为技术有限公司, 作品类别：美术 登记机构：, 登记号：国作登字-2020-F-00973503 登记日期：2020-01-17, 创作完成日期：2019-12-24 首次发表日期：,   
作品/制品, 作品名称：华为全连接开放实验室奖章 著作权人/权利人：华为技术有限公司, 作品类别：美术 登记机构：, 登记号：国作登字-2020-F-00973502 登记日期：2020-01-17, 创作完成日期：2019-12-24 首次发表日期：,   
作品/制品, 作品名称：X Labs5G动漫系列形象（小舞、小武） 著作权人/权利人：华为技术有限公司, 作品类别：美术 登记机构：, 登记号：国作登字-2019-F-00916679 登记日期：2019-11-20, 创作完成日期：2019-11-11 首次发表日期：,   
作品/制品, 作品名称：华为大数据魔力扑克 著作权人/权利人：华为技术有限公司, 作品类别：美术 登记机构：广东省版权保护联合会, 登记号：粤作登字-2019-F-00015229 登记日期：2019-08-20, 创作完成日期：2019-07-05 首次发表日期：,   
作品/制品, 作品名称：珍珠极光Pearl主题壁纸 著作权人/权利人：华为技术有限公司, 作品类别：美术 登记机构：, 登记号：国作登字-2019-F-00834615 登记日期：2019-08-19, 创作完成日期：2018-02-03 首次发表日期：2018-02-03,   
作品/制品, 作品名称：nova图标花纹样式设计方案 著作权人/权利人：华为技术有限公司, 作品类别：美术 登记机构：广东省版权保护联合会, 登记号：粤作登字-2019-F-00006099 登记日期：2019-04-30, 创作完成日期：2018-12-15 首次发表日期：,   
作品/制品, 作品名称：nova图标设计方案 著作权人/权利人：华为技术有限公司, 作品类别：美术 登记机构：广东省版权保护联合会, 登记号：粤作登字-2019-F-00006098 登记日期：2019-04-30, 创作完成日期：2018-12-15 首次发表日期：,   
作品/制品, 作品名称：虚拟AR女性形象Lysa 著作权人/权利人：华为技术有限公司, 作品类别：美术 登记机构：, 登记号：粤作登字-2018-F-00035309 登记日期：2018-12-29, 创作完成日期：2018-10-30 首次发表日期：,   
作品/制品, 作品名称：Design For Huawei图标设计方案 著作权人/权利人：华为技术有限公司, 作品类别：美术 登记机构：, 登记号：粤作登字-2017-F-00036062 登记日期：2017-12-18, 创作完成日期：2017-10-15 首次发表日期：,   
作品/制品, 作品名称：DevEco标志 著作权人/权利人：华为技术有限公司, 作品类别：美术 登记机构：, 登记号：粤作登字-2016-F-00017806 登记日期：2016-12-13, 创作完成日期：2016-01-31 首次发表日期：2016-02-22,   
作品/制品, 作品名称：华为产品定义社区吉祥兔 著作权人/权利人：华为技术有限公司, 作品类别：美术 登记机构：, 登记号：粤作登字-2016-F-00009116 登记日期：2016-08-10, 创作完成日期：2016-04-11 首次发表日期：2016-04-12,   
作品/制品, 作品名称：一种能力感知&amp;传播的用户界面（DevCloud ） 著作权人/权利人：华为技术有限公司, 作品类别：其他 登记机构：, 登记号：粤作登字-2016-L-00000607 登记日期：2016-07-25, 创作完成日期：2015-07-30 首次发表日期：2016-03-02,   
作品/制品, 作品名称：DevCloud logo 著作权人/权利人：华为技术有限公司, 作品类别：美术 登记机构：, 登记号：粤作登字-2016-F-00007533 登记日期：2016-07-11, 创作完成日期：2015-07-30 首次发表日期：2016-03-02,   
作品/制品, 作品名称：DevEco LOGO 著作权人/权利人：华为技术有限公司, 作品类别：美术 登记机构：, 登记号：粤作登字-2016-F-00007512 登记日期：2016-07-11, 创作完成日期：2016-01-31 首次发表日期：2016-02-22,   
作品/制品, 作品名称：一种研发系统的虚拟形象 著作权人/权利人：华为技术有限公司, 作品类别：美术 登记机构：, 登记号：粤作登字-2016-F-00007505 登记日期：2016-07-11, 创作完成日期：2016-01-31 首次发表日期：2016-02-22,   
作品/制品, 作品名称：DevCloud服务图标 著作权人/权利人：华为技术有限公司, 作品类别：美术 登记机构：, 登记号：粤作登字-2016-F-00007530 登记日期：2016-07-11, 创作完成日期：2015-07-30 首次发表日期：2016-03-02,   
作品/制品, 作品名称：一种游戏化的用户界面（DevEco ） 著作权人/权利人：华为技术有限公司, 作品类别：其他 登记机构：, 登记号：粤作登字-2016-L-00000432 登记日期：2016-06-15, 创作完成日期：2016-01-31 首次发表日期：2016-02-22,   
作品/制品, 作品名称：爱旅小海狮 著作权人/权利人：华为技术有限公司, 作品类别：美术 登记机构：, 登记号：粤作登字-2016-F-00003390 登记日期：2016-04-27, 创作完成日期：2015-04-02 首次发表日期：2015-05-28,   
作品/制品, 作品名称：一种杂志式的界面外观 著作权人/权利人：华为技术有限公司, 作品类别：其他 登记机构：, 登记号：粤作登字-2014-L-00000435 登记日期：2014-11-10, 创作完成日期：2014-07-15 首次发表日期：,   

'''
