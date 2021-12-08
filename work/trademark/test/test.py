# -*- coding: utf-8 -*-
# @Author: wangkun
# @Date: 2021-12-07 10:01:45
# @Descripttion:

import asyncio
import csv
import time

import nest_asyncio
import requests
from lxml import etree
from pyppeteer import launch
from user_agent import generate_user_agent

nest_asyncio.apply()


async def main():
    browser = await launch(headless=True, args=['--disable-infobars', '--no-sandbox'], userDataDir='/home/wkun/Temporary')
    page = await browser.newPage()
    await page.setUserAgent(generate_user_agent())
    await page.setJavaScriptEnabled(True)
    res = await page.goto('https://www.baidu.com', timeout=90000)
    a = res.status
    print(a)


if __name__ == '__main__':
    asyncio.run(main())
