# -*- coding: utf-8 -*-
# @Author: wangkun
# @Date: 2021-12-15 15:09:38
# @Descripttion:

import asyncio
import csv
import re
import time

import cv2 as cv
import nest_asyncio
import pytesseract
import redis
import requests
from lxml import etree
from PIL import Image
from pyppeteer import launch
from pyppeteer_stealth import stealth
from user_agent import generate_user_agent

nest_asyncio.apply()

# width = 1920w
# height = 1080
List = []


# 获取代理IP
def get_proxies():
    ip_url = "http://192.168.10.25:8000/ip"
    proxies = requests.get(ip_url, headers={'User-Agent': 'Mozilla/5.0'}).json()
    proxy = proxies['https'].split('@')[-1]
    print(proxy)
    return proxy


# 主函数
async def run():
    browser = await launch(headless=False, args=['--disable-infobars', '--no-sandbox'], userDataDir='/home/wkun/Temporary')
    page1 = await browser.newPage()
    # await stealth(page)
    # await page.setViewport({'width': width, 'height': height})
    await page1.setUserAgent(generate_user_agent())
    await page1.setJavaScriptEnabled(True)
    await page1.setViewport(viewport={'width': 1280, 'height': 800})
    await stealth(page1)
    # with open('C:/python/work/stealth.min.js') as f:
    #     js = f.read()
    # await page1.evaluateOnNewDocument("Page.addScriptToEvaluateOnNewDocument", {
    #     "source": js
    # })
    await page1.goto('https://www.whoscored.com/', timeout=90000)  # 打开网址，设定超时时间
    await asyncio.sleep(3)
    href_list = await page1.querySelectorAllEval('#today a.match-link.rc.preview', 'nodes => nodes.map(node => node.href)')
    for li in href_list:
        page = await browser.newPage()
        await stealth(page)
        await page.setUserAgent(generate_user_agent())
        await page.setJavaScriptEnabled(True)
        await page.setViewport(viewport={'width': 1280, 'height': 800})
        await page.goto(li)
        await page.waitForXPath('//*[@id="preview-lineups"]/div[1]/div[1]/div/a')
        text = await page.xpath('//*[@id="preview-lineups"]/div[1]/div[1]/div/a', 'node => getAttribute("textContent")')
        print(text)
    print(href_list, len(href_list))


if __name__ == '__main__':
    asyncio.run(run())
