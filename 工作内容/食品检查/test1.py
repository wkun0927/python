# encoding=utf-8
# 某一公司的合格信息

import random
import re
import time

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from user_agent import generate_user_agent


def getDriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")  # 禁用扩展
    options.add_argument("--disable-gpu")  # 谷歌文档提到需要加上这个属性来规避bug
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # options.add_argument('--headless')  # 无界面形式
    options.add_argument('--no-sandbox')  # 取消沙盒模式
    # options.add_argument('-kiosk')    # 全屏
    options.add_argument("--window-size=1920,1080")  # 指定浏览器分辨率
    # options.set_window_size(480, 600)  # 窗口大小变化
    options.add_argument('--disable-setuid-sandbox')
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument('--incognito')  # 启动进入隐身模式
    options.add_argument('--lang=zh-CN')  # 设置语言为简体中文
    options.add_argument('--user-agent={}'.format(generate_user_agent()))
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


# 左侧信息  检测合格
def left_info():
    # url需要拼接一下
    url_frame = 'https://spcjsac.gsxt.gov.cn/detail.html?type_id=&foodId='
    gongsi_name = '&goods_enterprise='

    header = {
        "cookie": "Hm_lvt_05faea25c554a42963bea18b02450589=1623982424; Hm_lpvt_05faea25c554a42963bea18b02450589=1623986542",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }
    time.sleep(5)
    for i in range(1, 11):  # 某一页中某公司的食品抽查记录，一页差不多有十条
        food_name = driver.find_element_by_xpath('//*[@id="main"]/div[3]/div[2]/div[1]/div/div[2]/table/tbody/tr[' + str(i) + ']/td[1]').get_attribute('outerHTML')
        # print(food_name)
        gongsi = re.findall(r'【.*?】', food_name)
        gongsi = str(str(str(gongsi).split('【')).split('】')).replace('"', '').replace("'", "").replace(" ", '').split(',')[1]
        # print(gongsi)
        id = re.findall(r'id=".*?" class', food_name)
        id = str(id).split('"')[1]
        # print(id)
        info = re.sub(u"\\<.*?\\>", "", food_name)
        print(info)
        food_url = url_frame + str(id) + gongsi_name + gongsi  # 食品抽查详细情况的url
        # print(food_url)
        try:  # 得到抽查详细信息
            time.sleep(random.randint(1, 2))
            driver1 = getDriver()
            driver1.get(food_url)
            jiancha_info = driver1.find_element_by_xpath('//*[@id="main"]/div[2]/div[2]/div[3]/div/div[1]').get_attribute('outerHTML')
            jiancha_info = re.sub(u"\\<.*?\\>", "", jiancha_info)
            print(jiancha_info)
            driver1.quit()
        except Exception as e:
            print(e)


if __name__ == '__main__':

    url = 'https://spcjsac.gsxt.gov.cn/'  # 搜索页
    driver = getDriver()
    driver.get(url)
    sel = Select(driver.find_element_by_xpath('//*[@id="main"]/div[3]/div[1]/div[1]/div/div/select'))  # 换到公司名查找
    sel.select_by_value('enterprisename')
    driver.find_element_by_xpath('//*[@id="main"]/div[3]/div[1]/div[2]/div/div/input').send_keys("三只松鼠")
    driver.find_element_by_xpath('//*[@id="main"]/div[3]/div[1]/div[3]/button').click()
    time.sleep(2)
    foot = driver.find_element_by_xpath('//*[@id="pager"]/div/div').get_attribute('innerHTML')
    page = str(re.findall(r'共\d页', foot))[3]  # 获取最后一页，因为最后一页的xpath有点不一样
    print(foot)
    print(page)
    if int(page) >= 5:
        i = 9
    else:
        i = 3 + int(page)
    try:
        left_info()  # 获取某一抽查的详细信息
        while True:  # 翻页
            driver.find_element_by_xpath('//*[@id="pager"]/div/div/ul/li[' + str(i) + ']/a').click()
            time.sleep(5)
            left_info()
    except:
        print('结束！')
    driver.quit()
'''

//*[@id="pager"]/div/div/ul/li[3]/a'
//*[@id="pager"]/div/div/ul/li[6]/a

'''
'''



'''
