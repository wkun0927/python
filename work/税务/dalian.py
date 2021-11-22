#encoding=utf-8

#税务违法   大连市信息获取

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

def getInfo(i):
    url='http://dalian.chinatax.gov.cn/module/jslib/bulletin2/lpindex.html'
    driver=getDriver()
    driver.get(url)
    driver.switch_to.frame('top')
    #纳税人名称
    nsrmc='大连永多贸易有限公司'
    #nsrmc='北京字节跳动科技有限公司'
    driver.find_element_by_xpath('//*[@id="na_name"]').send_keys(nsrmc)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="form1"]/button[1]').click()
    time.sleep(1)
    driver.switch_to.default_content()
    driver.switch_to.frame('right')

    result=driver.find_element_by_xpath('//*[@id="jpage"]').get_attribute('innerHTML')
    if re.findall(r"很遗憾，没有检索到任何记录！",result):
        print('无符合公布标准的案件信息')
        driver.quit()
        exit(0)
    else:
        #print(re.sub(u"\\<.*?\\>","",result))
        driver.find_element_by_xpath('//*[@id="jpage"]/div/div/table/tbody/tr/td/table[2]/tbody/tr['+str(i)+']/td[1]/a').click()
        driver.switch_to.default_content()
        time.sleep(1)
        driver.switch_to.frame('right')
        info=driver.find_element_by_xpath('/html/body/div[2]/div/table/tbody').get_attribute('innerHTML')
        #print(info)
        info1=info
        info2 = re.sub(u"\\</tr\\>", ",", info1)
        info3 = re.sub(u"\\</td\\>", "、", info2)
        info4 = re.sub(u"\\<.*?\\>", "", info3)
        info5 = re.sub(u"\n", "", info4)
        info6 = re.sub(u"\t", "", info5)
        info7 = re.sub(u"begin-->", "", info6)
        info8 = re.sub(u"end-->", "", info7)
        info8 = re.sub(u"\\<.*?\\>", ",", info8)
        info9 = info8.replace(' ', '').replace('、','').split(',')
        print(info9)

    driver.quit()

if __name__ == '__main__':
    try:
        for i in range(1,11):
            getInfo(i)
    except:
        exit(1)

'''

//*[@id="jpage"]/div/div/table/tbody/tr/td/table[2]/tbody/tr[1]/td[1]/a
//*[@id="jpage"]/div/div/table/tbody/tr/td/table[2]/tbody/tr[2]/td[1]/a

'''

'''

<tr>     
    <td align="center" style="line-height:30px;border-bottom:1px solid #CEE7E4;border-right:1px solid #CEE7E4;" width="300">检查机关

</td>     
    <td align="left" style="line-height:30px;padding-left:20px;border-bottom:1px solid #CEE7E4;word-break:break-

all;" width="500"><!--<$[税务机关名称全称]>begin-->国家税务总局大连市税务局第一稽查局<!--<$[税务机关名称全称]>end--></td>   
</tr> 
<tr>     
    <td align="center" style="line-height:30px;border-bottom:1px solid #CEE7E4;border-right:1px solid #CEE7E4;" width="300">所属年度

</td>     
    <td align="left" style="line-height:30px;padding-left:20px;border-bottom:1px solid #CEE7E4;word-break:break-

all;" width="500">2021年</td>   
</tr> 
<tr>     
    <td align="center" style="line-height:30px;border-bottom:1px solid #CEE7E4;border-right:1px solid #CEE7E4;" width="300">所属月份

</td>     
    <td align="left" style="line-height:30px;padding-left:20px;border-bottom:1px solid #CEE7E4;word-break:break-

all;" width="500">5月</td>   
</tr>   
<tr>     
    <td align="center" style="line-height:30px;border-bottom:1px solid #CEE7E4;border-right:1px solid #CEE7E4;" width="300">纳税人或者法人或者其他组织或者自然人名称</td>     
    <td align="left" style="line-height:30px;padding-left:20px;border-bottom:1px solid #CEE7E4;word-break:break-

all;" width="500"><!--<$[纳税人或者法人或者其他组织或者自然人名称]>begin-->大连永多贸易有限公司<!--<$[纳税人或者法人或者其他组织或者自然人名称]>end--></td>   
</tr>     
     
<tr>     
    <td align="center" style="line-height:30px;border-bottom:1px solid #CEE7E4;border-right:1px solid #CEE7E4;" width="300">组织机构代码</td>     
    <td align="left" style="line-height:30px;padding-left:20px;border-bottom:1px solid #CEE7E4;word-break:break-

all;" width="500"><!--<$[组织机构代码]>begin--><!--<$[组织机构代码]>end--></td>   
</tr>     
<tr>     
    <td align="center" style="line-height:30px;border-bottom:1px solid #CEE7E4;border-right:1px solid #CEE7E4;" width="300">注册地址</td>     
    <td align="left" style="line-height:30px;padding-left:20px;border-bottom:1px solid #CEE7E4;word-break:break-

all;" width="500"><!--<$[注册地址]>begin-->辽宁省大连市中山区长江路29号12层1207-7<!--<$[注册地址]>end--></td>   
</tr>     
<tr>     
    <td align="center" style="line-height:30px;border-bottom:1px solid #CEE7E4;border-right:1px solid #CEE7E4;" width="300">法定代表人或负责人或经法院裁判确定的实际责任人</td>     
    <td align="left" style="line-height:30px;padding-left:20px;border-bottom:1px solid #CEE7E4;word-break:break-

all;" width="500"><!--<$[法定代表人或负责人或经法院裁判确定的实际责任人]>begin-->杨猛<!--<$[法定代表人或负责人或经法院裁判确定的实际责任人]>end--></td>   
</tr>     
<tr>     
    <td align="center" style="line-height:30px;border-bottom:1px solid #CEE7E4;border-right:1px solid #CEE7E4;" width="300">法定代表人或者负责人性别</td>     
    <td align="left" style="line-height:30px;padding-left:20px;border-bottom:1px solid #CEE7E4;word-break:break-

all;" width="500"><!--<$[法定代表人或者负责人性别]>begin-->男性<!--<$[法定代表人或者负责人性别]>end--></td>   
</tr>     
<tr>     
    <td align="center" style="line-height:30px;border-bottom:1px solid #CEE7E4;border-right:1px solid #CEE7E4;" width="300">法定代表人或者负责人证件名称</td>     
    <td align="left" style="line-height:30px;padding-left:20px;border-bottom:1px solid #CEE7E4;word-break:break-

all;" width="500">身份证</td>   
</tr>     
<tr>     
    <td align="center" style="line-height:30px;border-bottom:1px solid #CEE7E4;border-right:1px solid #CEE7E4;" width="300">法定代表人或者负责人证件号码</td>     
    <td align="left" style="line-height:30px;padding-left:20px;border-bottom:1px solid #CEE7E4;word-break:break-

all;" width="500"><!--<$[法定代表人或者负责人证件号码]>begin-->210726********1530<!--<$[法定代表人或者负责人证件号码]>end--></td>   
</tr> 
<tr>     
    <td align="center" style="line-height:30px;border-bottom:1px solid #CEE7E4;border-right:1px solid #CEE7E4;" width="300">经法院裁判负直接责任的财务人员姓名</td>     
    <td align="left" style="line-height:30px;padding-left:20px;border-bottom:1px solid #CEE7E4;word-break:break-

all;" width="500"><!--<$[经法院裁判负直接责任的财务人员姓名]>begin--><!--<$[经法院裁判负直接责任的财务人员姓名]>end--></td>   
</tr>
<tr>     
    <td align="center" style="line-height:30px;border-bottom:1px solid #CEE7E4;border-right:1px solid #CEE7E4;" width="300">负有直接责任的财务负责人性别</td>     
    <td align="left" style="line-height:30px;padding-left:20px;border-bottom:1px solid #CEE7E4;word-break:break-

all;" width="500"><!--<$[负有直接责任的财务负责人性别]>begin--><!--<$[负有直接责任的财务负责人性别]>end--></td>   
</tr>
<tr>     
    <td align="center" style="line-height:30px;border-bottom:1px solid #CEE7E4;border-right:1px solid #CEE7E4;" width="300">负有直接责任的财务负责人证件名称</td>     
    <td align="left" style="line-height:30px;padding-left:20px;border-bottom:1px solid #CEE7E4;word-break:break-

all;" width="500"></td>   
</tr>
<tr>     
    <td align="center" style="line-height:30px;border-bottom:1px solid #CEE7E4;border-right:1px solid #CEE7E4;" width="300">负有直接责任的财务负责人证件号码</td>     
    <td align="left" style="line-height:30px;padding-left:20px;border-bottom:1px solid #CEE7E4;word-break:break-

all;" width="500"><!--<$[负有直接责任的财务负责人证件号码]>begin--><!--<$[负有直接责任的财务负责人证件号码]>end--></td>   
</tr>
<tr>     
    <td align="center" style="line-height:30px;border-bottom:1px solid #CEE7E4;border-right:1px solid #CEE7E4;" width="300">负有直接责任的中介机构信息及其从业人员信息</td>     
    <td align="left" style="line-height:30px;padding-left:20px;border-bottom:1px solid #CEE7E4;word-break:break-

all;" width="500"><!--<$[负有直接责任的中介机构信息及其从业人员信息]>begin--><!--<$[负有直接责任的中介机构信息及其从业人员信息]>end--></td>   
</tr>
<tr>     
    <td align="center" style="line-height:30px;border-bottom:1px solid #CEE7E4;border-right:1px solid #CEE7E4;" width="300">案件性质</td>     
    <td align="left" style="line-height:30px;padding-left:20px;border-bottom:1px solid #CEE7E4;word-break:break-

all;" width="500"><!--<$[案件性质全称]>begin-->走逃（失联）<!--<$[案件性质全称]>end--></td>   
</tr>
<tr>     
    <td align="center" style="line-height:30px;border-bottom:1px solid #CEE7E4;border-right:1px solid #CEE7E4;" width="300">主要违法事实</td>     
    <td align="left" style="line-height:30px;padding-left:20px;border-bottom:1px solid #CEE7E4;word-break:break-

all;" width="500"><!--<$[主要违法事实]>begin-->经国家税务总局大连市税务局第一稽查局检查，发现其在2017年01月01日至2019年12月31日期间，主要存在以下问题：对外虚开普通发票125份，票面额累计959.79万元。经国家税务总局大连市税务局第一稽查局查证确认走逃（失联）,已发布走逃（失联）纳税人公告。<!--<$[主要违法事实]>end--></td>   
</tr>
<tr>     
    <td align="center" style="line-height:30px;border-bottom:1px solid #CEE7E4;border-right:1px solid #CEE7E4;" width="300">相关法律依据及税务处理处罚情况</td>     
    <td align="left" style="line-height:30px;padding-left:20px;border-bottom:1px solid #CEE7E4;word-break:break-

all;" width="500"><!--<$[相关法律依据及税务处理处罚情况]>begin-->依照《中华人民共和国税收征收管理法》等相关法律法规的有关规定，依法移送公安机关。<!--<$[相关法律依据及税务处理处罚情况]>end--></td>   
</tr>


'''