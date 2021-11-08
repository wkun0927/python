#encoding=gbk
#澎湃新闻   测试
from selenium import webdriver
import time
import re
def get_info(url):
    text_list=[]
    # option=webdriver.ChromeOptions(),options=option
    # option.add_argument('headless')
    driver=webdriver.Chrome(executable_path='F:\\chromedriver.exe')

    driver.get(url)
    #time.sleep(20)
    key_words='字节跳动'
    #driver.find_element_by_name('inpsearch').send_keys(key_words)
    #driver.find_element_by_xpath('//*[@id="search_key"]').click()
    #print(driver.page_source)
    try:            #获取正文


        title=driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/h1').get_attribute('innerHTML')
        #print(title)
        text_list.append(title)
        t1=driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/div[2]/p[1]').get_attribute('innerHTML')
        #print(t1)
        text_list.append(t1)
        t2 = driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/div[2]/p[2]').get_attribute('innerHTML')
        # print(t1)
        text_list.append(t2)
        text=driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/div[3]').get_attribute('innerHTML')
        text_list.append(text)
        #print(driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/div[3]').get_attribute('innerHTML'))

    except:
        pass
    print(text_list)
    driver.quit()


#url='https://www.thepaper.cn/newsDetail_forward_12543477'
url='https://www.thepaper.cn/newsDetail_forward_12483801'

get_info(url)
