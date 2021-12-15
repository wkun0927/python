#encoding=utf-8

import requests
from selenium import webdriver
import time
import re


header={
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "cookie": "IPLOC=CN1100; SUV=210518172217VPZ5; gidinf=x099980109ee135a8f0263c71000eb4c7cd0263a7f33; jv=6deab5ccb5c6d821435410d83aa5f9e0-ZoAo4pLC1621330262970; reqtype=pc; BAIDU_SSP_lcr=https://pos.baidu.com/; t=1622101229033"
}
# option=webdriver.ChromeOptions(),options=option
# option.add_argument('headless')

#获取搜索页内容
def get_info(url):
    info_list=[]
    option=webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(executable_path='F:\\chromedriver.exe',options=option)
    driver.get(url)
    time.sleep(5)
    try:
        for i in range(1,50):
            info_list=[]
            title=driver.find_element_by_xpath('//*[@id="news-list"]/div['+str(i)+']/div/div[2]/div').get_attribute('innerHTML')
            #print(title)
            link=str(title).split('"')[1]
            info_list.append(link)

            #print(link)
            title = re.sub(u"\\<.*?\\>", "", title)
            #print(title)
            info_list.append(title)
            source=driver.find_element_by_xpath('//*[@id="news-list"]/div['+str(i)+']/div/div[2]/p[2]').get_attribute('innerHTML')
            source = re.sub(u"\\<.*?\\>", "", source)
            source = re.sub(u"\n*", "", source)
            source = re.sub(u"&nbsp;*", "", source)
            source = re.sub(u" ", "", source)
            #print(source)
            info_list.append(source)
            print(info_list)
            get_text(link)
    except:
        print(111)
    driver.quit()
    #return info_list

#获取正文内容
def get_text(url):

    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(executable_path='F://chromedriver.exe',options=option)
    driver.get(url)
    try:        #每一段落的文字
        for i in range(1, 50):
            path = '//*[@id="mp-editor"]/p[' + str(i) + ']'
            t1 = driver.find_element_by_xpath(path).get_attribute('innerHTML')
            t1 = re.sub(u"\\<.*?\\>", '', t1)
            print(t1)
    except:
        pass

    driver.quit()


url='https://search.sohu.com/?keyword=字节跳动&spm=smpc.csrpage.0.0.1622101065061ECAfnnc&queryType=edit'
#all_list=get_info(url)
get_info(url)

