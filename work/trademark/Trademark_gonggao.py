# -*- coding: utf-8 -*-
# @Author: wangkun
# @Date: 2021-12-07 11:39:37
# @Descripttion:

import asyncio
import csv
import time

import nest_asyncio
import redis
import requests
from lxml import etree
from pyppeteer import launch
from user_agent import generate_user_agent

nest_asyncio.apply()

# width = 1920w
# height = 1080
List = []


# 获取代理IP
def get_proxies():
    ip_url = "http://192.168.10.25:8000/ip"
    proxies = requests.get(ip_url, headers={
        'User-Agent': 'Mozilla/5.0'
    }).json()
    print(proxies)
    proxy = 'http://' + proxies['http'].split('@')[-1]
    return proxy


# 主函数
async def run():
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    count = '华为技术有限公司'  # 初始申请人
    browser = await launch(headless=False, args=['--disable-infobars', '--no-sandbox'], userDataDir='/home/wkun/Temporary')
    # browser = await launch(headless=False, args=['--disable-infobars', '--no-sandbox'], userDataDir='D:/Temporary')
    page1 = await browser.newPage()
    # await stealth(page)
    # await page.setViewport({'width': width, 'height': height})
    await page1.setUserAgent(generate_user_agent())
    await page1.setJavaScriptEnabled(True)

    await page1.goto('http://sbj.cnipa.gov.cn/', timeout=90000)  # 打开网址，设定超时时间
    await asyncio.sleep(10)
    await (await page1.xpath('//*[@class="bscont12 bscont"]//a'))[0].click()  # 点击“商标公告”

    await asyncio.sleep(5)
    page_list = await browser.pages()  # 切换焦点网页
    page2 = page_list[-1]

    await page2.waitForNavigation({'timeout': 50000})
    await page2.click('tr:nth-child(2)>td:nth-child(1)')  # 点击期号
    await asyncio.sleep(15)


if __name__ == '__main__':
    asyncio.run(run())
