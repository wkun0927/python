#coding=utf-8
import requests
import lxml
from selenium import webdriver

#   获取图片测试页
# url_prefix='https:'
# url_pict='//n.sinaimg.cn/sinakd20210529ac/213/w2048h1365/20210529/7e8b-kquziii3577555.jpg'
# url=url_prefix+url_pict

url='https://t.cj.sina.com.cn/articles/view/7138030437/1a975b36500100xykb'

driver=webdriver.Chrome(executable_path='F:\\chromedriver.exe')
f=open('pict.jpg', 'wb')
driver.get(url)
te=driver.find_element_by_id('article-img').get_attribute('outerHTML')
print(te)
# f.write(response.content)
f.close()
driver.quit()