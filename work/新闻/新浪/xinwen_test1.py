#腾讯新闻内容爬取

# encoding=utf-8

import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import re


#获取正文内容和图片
def get_text(url):
    option=webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(executable_path='F:\\chromedriver.exe')
    #print(url)
    driver.get(url)
    text_list = []
    try:       #获取正文
        for i in range(1,50):
            ti=driver.find_element_by_xpath('//*/p['+str(i)+']').get_attribute('innerHTML')
            tii=re.sub(u"\\<.*?\\>","",ti)
            text_list.append(tii)
    except:
        pass
    try:    #获取图片
        for i in range(1, 50):
            src = driver.find_element_by_xpath('//*[@id="artibody"]/div[' + str(i) + ']').get_attribute('innerHTML')
            #print(src)
            src1 = re.findall(r'//n.sina[\s\S]*jpg|//n.sina[\s\S]*png', src)
            #print(src1)
            if src1==[]:
                pass
            else:
                url_pict = url_prefix + src1[0]
                print(2,url_pict)
                pict_addr = url_pict.split('/')[-1]
                print(3,pict_addr)
                f = open(pict_addr, 'wb')
                response = requests.get(url_pict)
                f.write(response.content)
                f.close()

    except:
        print(text_list)
    all_list.append(text_list)
    all_list.append('')
    driver.quit()


def get_url(url):   #通过搜索页获取正文链接

    response=requests.get(url).text
    soup=BeautifulSoup(response,'html.parser')
    alink=soup.select('h2')

    for link in alink:
        #print(link.text)
        all_list.append(link.text)
        url_link=str(link).split('"')[1]
        print(url_link)
        all_list.append(url_link)
        get_text(url_link)

if __name__=='__main__':
    url_prefix = 'https:'
    url='https://search.sina.com.cn/news?q=字节跳动&c=news&from=index&range=all&size=10&dpc=0&ps=0&pf=0&page=1'
    all_list=[]
    get_url(url)


