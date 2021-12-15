# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-12-09 19:08:44
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
    browser = await launch(headless=True, args=['--disable-infobars', '--no-sandbox'], userDataDir='C:/Temporary')
    page1 = await browser.newPage()
    await stealth(page1)
    # with open('C:/python/work/stealth.min.js') as f:
    #     js = f.read()
    # await page1.evaluateOnNewDocument("Page.addScriptToEvaluateOnNewDocument", {
    #     "source": js
    # })
    # await stealth(page)
    # await page.setViewport({'width': width, 'height': height})
    await page1.setUserAgent(generate_user_agent())
    await page1.setJavaScriptEnabled(True)
    await page1.setViewport(viewport={'width': 1280, 'height': 800})
    # await page1.goto('https://bot.sannysoft.com/', timeout=90000)  # 打开网址，设定超时时间
    await page1.goto('https://www.whoscored.com/', timeout=90000)
    html = await page1.content()
    print(html)
    await browser.close()


if __name__ == '__main__':
    asyncio.run(run())
