#encoding=utf-8

#税务违法   吉林信息获取

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
    url = 'http://jilin.chinatax.gov.cn/col/col19972/index.html'
    driver = getDriver()
    driver.get(url)
    # 纳税人名称
    nsrmc = '长春市润宝泰经贸有限公司'
    # nsrmc='北京字节跳动科技有限公司'
    driver.find_element_by_xpath('//*[@id="searchTable"]/tbody/tr[1]/td[2]/input').send_keys(nsrmc)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="fgk-select"]').click()
    time.sleep(1)
    driver.switch_to.frame('showIframe')
    result = driver.find_element_by_xpath('/html/body/form/div/div/span').get_attribute('innerHTML')
    #print(result)
    if re.findall(r"共&nbsp;0&nbsp;页", result):
        print('无符合公布标准的案件信息')
        driver.quit()
        exit(0)
    else:
        # print(re.sub(u"\\<.*?\\>","",result))
        driver.find_element_by_xpath('/html/body/div/table[3]/tbody/tr['+str(i)+']/td[5]/a').click()
        all_h = driver.window_handles
        driver.switch_to.window(all_h[1])
        info = driver.find_element_by_xpath('//*[@id="barrierfree_container"]/div[3]/div/table/tbody').get_attribute('innerHTML')
        info1 = re.sub(u"<script>.*?</script>", ",", info)
        info2 = re.sub(u"\\</tr\\>", ",", info1)
        info3 = re.sub(u"\\</td\\>", "、", info2)
        info4 = re.sub(u"\\<.*?\\>", "", info3)
        info5 = re.sub(u"\n", "", info4)
        info6 = re.sub(u"\t", "", info5)
        info7 = re.sub(u"begin-->", "", info6)
        info8 = re.sub(u"end-->", "", info7)
        info9 = info8.replace(' ', '').split(',')
        print(info9)
    driver.quit()

if __name__ == '__main__':
    try:
        for i in range(2,11,2):
            getInfo(i)
    except:
        exit(1)



'''
/html/body/div/table[3]/tbody/tr[2]/td[5]/a
/html/body/div/table[3]/tbody/tr[4]/td[5]/a
/html/body/div/table[3]/tbody/tr[10]/td[5]/a

<tr>
    		<td class="title_left" width="22%">纳税人名称</td>
    		<td width="78%" class="blue14"><script>$(function(){ $('*',$('form.comment')).attr('disabled', 'disabled');}); </script>
<!--<$[纳税人名称]>begin-->长春市润宝泰经贸有限公司<!--<$[纳税人名称]>end-->
</td>
    	</tr>
    	<tr>
    		<td class="title_left" width="22%">纳税人识别号或社会信用代码</td>
    		<td width="78%"><script>$(function(){ $('*',$('form.comment')).attr('disabled', 'disabled');}); </script>
<!--<$[纳税人识别号]>begin-->91220104MA143GH35R<!--<$[纳税人识别号]>end-->
</td>
    	</tr>
    	<tr>
    		<td class="title_left" width="22%">组织机构代码</td>
    		<td width="78%"><script>$(function(){ $('*',$('form.comment')).attr('disabled', 'disabled');}); </script>
<!--<$[组织机构代码]>begin--><!--<$[组织机构代码]>end-->
</td>
    	</tr>
    	<tr>
    		<td class="title_left" width="22%">注册地址</td>
    		<td width="78%"><script>$(function(){ $('*',$('form.comment')).attr('disabled', 'disabled');}); </script>
<!--<$[注册地址]>begin-->吉林省长春市朝阳区安达街东、西安大路南盛嘉新城2栋1010-4室<!--<$[注册地址]>end-->
</td>
    	</tr>
    	<tr>
    		<td class="title_left" width="22%">法定代表人或者负责人姓名、性别及身份证号码（或其他证件号码）</td>
    		<td width="78%"><script>$(function(){ $('*',$('form.comment')).attr('disabled', 'disabled');}); </script>
<!--<$[法定代表人或负责人姓名]>begin-->杨继生<!--<$[法定代表人或负责人姓名]>end-->，<!--<$[性别]>begin-->男性<!--<$[性别]>end-->，<!--<$[法定代表人或者负责人证件号码]>begin-->220104********2412<!--<$[法定代表人或者负责人证件号码]>end-->
</td>
    	</tr>
    	<tr>
    		<td class="title_left" width="22%">违法期间法人代表姓名及身份证号码</td>
    		<td width="78%"><script>$(function(){ $('*',$('form.comment')).attr('disabled', 'disabled');}); </script>
<!--<$[违法期间法人代表姓名]>begin--><!--<$[违法期间法人代表姓名]>end--><!--<$[违法期间法人身份证号码]>begin--><!--<$[违法期间法人身份证号码]>end-->
</td>
    	</tr>
    	<tr>
    		<td class="title_left" width="22%">负有直接责任的财务人员姓名、性别及身份证号码（或其他证件号码）</td>
    		<td width="78%"><script>$(function(){ $('*',$('form.comment')).attr('disabled', 'disabled');}); </script>
<!--<$[负有直接责任的财务负责人姓名]>begin--><!--<$[负有直接责任的财务负责人姓名]>end--><!--<$[负有直接责任的财务负责人性别]>begin--><!--<$[负有直接责任的财务负责人性别]>end--><!--<$[负有直接责任的财务负责人证件号码]>begin--><!--<$[负有直接责任的财务负责人证件号码]>end-->
</td>
    	</tr>
    	<tr>
    		<td class="title_left" width="22%">实际负责人姓名、性别及身份证号码（或其他证件号码）</td>
    		<td width="78%"><script>$(function(){ $('*',$('form.comment')).attr('disabled', 'disabled');}); </script>
<!--<$[实际负责人姓名]>begin--><!--<$[实际负责人姓名]>end--><!--<$[实际负责人性别]>begin--><!--<$[实际负责人性别]>end--><!--<$[实际负责人证件号码]>begin--><!--<$[实际负责人证件号码]>end-->
</td>
    	</tr>
    	<tr>
    		<td class="title_left" width="22%">负有直接责任的中介机构信息</td>
    		<td width="78%"><script>$(function(){ $('*',$('form.comment')).attr('disabled', 'disabled');}); </script>
<!--<$[中介机构信息及其从业人员信息]>begin--><!--<$[中介机构信息及其从业人员信息]>end-->
</td>
    	</tr>
    	<tr>
    		<td class="title_left" width="22%">案件性质</td>
    		<td width="78%"><script>$(function(){ $('*',$('form.comment')).attr('disabled', 'disabled');}); </script>
<!--<$[案件性质]>begin-->虚开普通发票<!--<$[案件性质]>end-->
</td>
    	</tr>
    	<tr>
    		<td class="title_left" width="22%">主要违法事实相关法律依据及税务处理处罚情况</td>
    		<td width="78%"><script>$(function(){ $('*',$('form.comment')).attr('disabled', 'disabled');}); </script>
<!--<$[主要违法事实]>begin-->经国家税务总局长春市税务局稽查局检查，发现其在2017年03月28日至2020年08月26日期间，主要存在以下问题：对外虚开普通发票2500份，票面额累计1089.07万元。<!--<$[主要违法事实]>end-->，<!--<$[相关法律依据及税务处理处罚情况]>begin-->依照《中华人民共和国税收征收管理法》等相关法律法规的有关规定，对其依法移送司法机关。<!--<$[相关法律依据及税务处理处罚情况]>end-->
</td>
    	</tr>
		<tr>
    		<td colspan="2" style="padding: 20px 0; background: #f3f8fd;">
    	   	 <a style="padding: 5px 10px; background: #0064B1; color: #ffffff; " href="javascript:window.print()" class="leftleft">打印本页</a></td>
    	</tr>

'''