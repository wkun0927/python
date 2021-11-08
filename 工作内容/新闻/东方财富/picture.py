# coding=utf-8
import requests
import lxml

url = 'https://dfscdn.dfcfw.com/download/A202PDJW2YTR0G3'
f = open('pict1.jpg', 'wb')
response = requests.get(url)
f.write(response.content)
f.close()
