#encoding=gbk
import requests
from selenium import webdriver
import re

#获取正文页内容测试

url='http://www.sohu.com/a/455347684_120638843?scm=1019.e000a.v1.0&amp;spm=smpc.csrpage.news-list.1.1622106448870EY35pD9'
option=webdriver.ChromeOptions()
option.add_argument('headless')
driver=webdriver.Chrome(executable_path='F://chromedriver.exe')
driver.get(url)
# t1=driver.find_element_by_xpath('//*[@id="mp-editor"]/p[1]').get_attribute('innerHTML')
# t1=re.sub(u"\\<.*?\\>",'',t1)
# print(t1)
try:
    for i in range(1,50):
        path='//*[@id="mp-editor"]/p['+str(i)+']'
        #print(path)
        t1=driver.find_element_by_xpath(path).get_attribute('innerHTML')
        t1=re.sub(u"\\<.*?\\>",'',t1)
        print(t1)
except:
    pass




driver.quit()



