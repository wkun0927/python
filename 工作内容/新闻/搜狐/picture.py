#coding=utf-8
import requests
import lxml
from selenium import webdriver

driver=webdriver.Chrome(executable_path='F://chromedriver.exe')
url='http://www.sohu.com/a/455347684_120638843?scm=1019.e000a.v1.0&amp;spm=smpc.csrpage.news-list.1.1622106448870EY35pD9'
driver.get(url)
try:    #测试   得到图片url，然后保存下来
    for i in range(1,20):
        p1=driver.find_element_by_xpath('//*[@id="mp-editor"]/p[4['+str(i)+']/img').get_attribute('value')
        print(p1)
        img_addr=str(p1).split('"')[-2]
        #print(img_addr)
        response=requests.get(img_addr)
        name=img_addr.split('/')[-1]

        f=open(name, 'wb')
        f.write(response.content)
        f.close()
except:
    pass

driver.quit()


'''
//*[@id="mp-editor"]/p[4]/img
//*[@id="mp-editor"]/p[7]/img
'''