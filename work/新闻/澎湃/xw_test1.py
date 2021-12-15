#encoding=gbk
#澎湃新闻
from selenium import webdriver
import time
import re
import requests


def get_info(url):
    # option=webdriver.ChromeOptions(),options=option
    # option.add_argument('headless')
    driver=webdriver.Chrome(executable_path='F:\\chromedriver.exe')

    driver.get(url)
    time.sleep(10)
    key_words='字节跳动'        #传参点击搜索
    driver.find_element_by_name('inpsearch').send_keys(key_words)
    driver.find_element_by_xpath('//*[@id="search_key"]').click()
    print(driver.page_source)
    try:
        article_name1=driver.find_element_by_xpath('//*[@id="mainContent"]/div[1]/h2').get_attribute('innerHTML')
        url_mod(article_name1)
        article_name2=driver.find_element_by_xpath('//*[@id="mainContent"]/div[2]/h2').get_attribute('innerHTML')
        url_mod(article_name2)
        article_name3=driver.find_element_by_xpath('//*[@id="mainContent"]/div[3]/h2').get_attribute('innerHTML')
        url_mod(article_name3)
        # article_name4=driver.find_element_by_xpath('//*[@id="mainContent"]/div[4]/h2').get_attribute('innerHTML')
        # url_mod(article_name4)
        # article_name5=driver.find_element_by_xpath('//*[@id="mainContent"]/div[5]/h2').get_attribute('innerHTML')
        # url_mod(article_name5)
    except:
        pass
    driver.quit()

def url_mod(article_name):  #获取正文链接   url需要自己拼接
    title1 = re.sub(u'\n\t*','',article_name)
    title2 = re.sub(u"\\<.*?\\>", "", title1)
    title = title2.replace(' ', '')
    print(title)
    url_prefix = 'https://www.thepaper.cn/'
    link = re.findall(r'href="[\s\S]*" target', article_name)
    #print(link)
    #f.write(link)
    url_m = url_prefix + str(link).split('"')[1]
    print(url_m)
    #f.write(url_m)
    #text_list.append(title)
    #text_list.append(url_m)
    get_text_info(url_m)


def get_text_info(url):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver=webdriver.Chrome(executable_path='F:\\chromedriver.exe',options=option)
    driver.get(url)
    time.sleep(10)
    try:        #获取正文
        #title=driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/h1').get_attribute('innerHTML')
        #print(title)
        #text_list.append(title)
        #f.write(title)
        t1=driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/div[2]/p[1]').get_attribute('innerHTML')
        print(t1)
        #text_list.append(t1)
        #f.write(t1)
        t2 = driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/div[2]/p[2]').get_attribute('innerHTML')
        t21=re.sub(u'\\<.*?\\>','',t2)
        t22=re.sub('\n','',t21)
        t23=re.sub(' ','',t22)
        print(t23)
        text=driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/div[3]').get_attribute('innerHTML')
        print(text)
        #text_list.append(text)
        #print(driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/div[3]').get_attribute('innerHTML'))
    except:
        pass
    try:        #获取图片
        for i in range(1, 10):
            p1 = driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/div[3]/img[' + str(i) + ']').get_attribute('outerHTML')
            # print(p1)
            img_addr = str(p1).split('"')[-2]
            # print(img_addr)
            response = requests.get(img_addr)
            name = img_addr.split('/')[-1]

            f = open(name, 'wb')
            f.write(response.content)
            f.close()
    except:
        pass
    #text_list.append('end')
    driver.quit()

if __name__=='__main__':
    url='https://www.thepaper.cn/searchResult.jsp'
    get_info(url)   #获取新闻信息



