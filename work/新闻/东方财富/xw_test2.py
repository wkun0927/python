# coding=utf-8

from selenium import webdriver
import re
import requests

option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome(executable_path='F://chromedriver.exe', options=option)
url = 'http://finance.eastmoney.com/a/202004241466514052.html'
driver.get(url)

try:  # 获取图片
    pict = driver.find_element_by_xpath('//*[@id="ContentBody"]/center[1]').get_attribute('innerHTML')
    print(pict)
    src_pict = str(pict).split('"')[1]
    print(src_pict)
    name = src_pict.split('/')[-1]
    f = open(name + '1.jpg', 'wb')
    response = requests.get(src_pict)
    f.write(response.content)
    f.close()

except:
    pass

# source=driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]').get_attribute('innerHTML')
# source1=re.sub(u"\\<.*?\\>","",source)
# source2=re.sub(u" ","",source1)
# source3=re.sub(u"\n*","",source2)
# print(source3)
# text_list=[]
# try:  获取正文
#     for i in range(1,20):
#         text=driver.find_element_by_xpath('//*[@id="ContentBody"]/p['+str(i)+']').get_attribute('innerHTML')
#         text1=re.sub(u"\\<.*?\\>","",text)
#         text2=re.sub(u" ","",text1)
#         text3=re.sub(u"\u3000","",text2)
#         text4 = re.sub(u"\n", "", text3)
#         text5 = re.sub(u"&gt;", "", text4)
#         text_list.append(text5)
# except:
#     pass
# print(text_list)

driver.quit()
