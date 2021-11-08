#coding=gbk
from selenium import webdriver
import re
import requests

        #测试页 获取图片


# option=webdriver.ChromeOptions(),options=option
# option.add_argument('headless')
driver=webdriver.Chrome(executable_path='F:\\chromedriver.exe')
url='http://k.sina.com.cn/article_1664221137_6331ffd102000w9rn.html'
url='https://finance.sina.com.cn/stock/relnews/cn/2021-05-28/doc-ikmyaawc8098782.shtml'
#url='https://n.sinaimg.cn/sinakd20210529ac/213/w2048h1365/20210529/7e8b-kquziii3577555.jpg'
url_prefix='https:'
driver.get(url)

text_list=[]
try:
    for i in range(1, 2):
        #t1=driver.find_element_by_xpath('//*/p[' + str(i) + ']').get_attribute('innerHTML')
        #text_list.append(driver.find_element_by_xpath('//*/p[' + str(i) + ']').get_attribute('innerHTML'))
        src=driver.find_element_by_xpath('//*[@id="artibody"]/div[' + str(i) + ']').get_attribute('innerHTML')
        print(src)
        print(2)

        src1=re.findall(r'//n.sina[\s\S]*jpg|//n.sina[\s\S]*png',src)
        print(src1)
        print(1)
        url_pict=url_prefix+src1[0]
        print(url_pict)
        pict_addr = str(src1[0]).split('/')[-1]
        print(pict_addr)
        f = open(pict_addr, 'wb')
        response = requests.get(url_pict)
        f.write(response.content)
        f.close()

except:
    pass

#print(text_list)
driver.quit()

