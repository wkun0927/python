# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-07-26 09:31:49
# @Description: pyppeteer

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
    return proxies['http']


def recognize_text(img_path):
    # 打开文件夹中的图片
    image = Image.open(img_path)
    # 灰度图
    lim = image.convert('L')
    # 灰度阈值设为165，低于这个值的点全部填白色
    threshold = 150
    table = []

    for j in range(256):
        if j < threshold:
            table.append(0)
        else:
            table.append(1)

    bim = lim.point(table, '1')
    bim.save(img_path)
    text = pytesseract.image_to_string(bim)
    text = re.findall('\d+', text)
    text = ''.join(text)
    print(text)
    return text


# 主函数
async def run():
    img_path = 'C:/python/work/trademark/img/yanzhengma.png'
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    count = '华为技术有限公司'  # 初始申请人
    browser = await launch(headless=False, args=['--disable-infobars', '--no-sandbox'], userDataDir='C:/Temporary')
    # browser = await launch(headless=False, args=['--disable-infobars', '--no-sandbox'], userDataDir='D:/Temporary')
    page1 = await browser.newPage()
    # await stealth(page)
    # await page.setViewport({'width': width, 'height': height})
    await page1.setUserAgent(generate_user_agent())
    await page1.setJavaScriptEnabled(True)
    with open('C:/python/work/stealth.min.js') as f:
        js = f.read()
    await page1.evaluateOnNewDocument("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
    })
    await page1.goto('http://sbj.cnipa.gov.cn/', timeout=90000)  # 打开网址，设定超时时间
    await asyncio.sleep(10)
    await (await page1.xpath('//*[@class="bscont2 bscont"]//a'))[0].click()  # 点击“商标网上查询”

    await asyncio.sleep(5)
    page_list = await browser.pages()  # 切换焦点网页
    page2 = page_list[-1]
    await (await page2.xpath('//div[@class="TRS_Editor"]//img'))[0].click()  # 我接受

    await page2.waitForNavigation({'timeout': 50000})
    try:
        yanzhengma = await page2.select('#AREA > div > img')
        await yanzhengma.screenshot({'path': 'C:/python/work/trademark/img/yanzhengma.png'})
        text = recognize_text(img_path)
        await page2.type('#answer', text)
        await page2.click('#check')
    except Exception as e:
        print(e)
        pass
    await page2.click('.icon_box>[src="/tmrp/images/icon2.png"]')  # 点击商标综合查询xx
    await asyncio.sleep(5)
    try:
        yanzhengma = await page2.select('#AREA > div > img')
        await yanzhengma.screenshot({'path': 'C:/python/work/trademark/img/yanzhengma.png'})
        text = recognize_text(img_path)
        await page2.type('#answer', text)
        await page2.click('#check')
    except Exception as e:
        print(e)
        pass
    try:
        await page2.type('[name="request:hnc"]', count)  # 输入注册号
        await asyncio.sleep(2)
        await page2.click('#_searchButton')  # 点击查询按钮
        await asyncio.sleep(5)
        page_list = await browser.pages()
        print(page_list)
        page3 = page_list[-1]
        try:
            yanzhengma = await page3.select('#AREA > div > img')
            await yanzhengma.screenshot({'path': 'C:/python/work/trademark/img/yanzhengma.png'})
            text = recognize_text(img_path)
            await page2.type('#answer', text)
            await page2.click('#check')
        except Exception as e:
            print(e)
            pass
        while True:
            item = dict()
            await page3.waitForXPath('//tr[@class="ng-scope"]/td', timeout=90000)
            # 获取网页内容并提取数据
            text = await page3.content()
            html = etree.HTML(text)
            for i in range(1, 51):
                pic_url = html.xpath('//tr[@class="ng-scope"][' + str(i) + ']//input/@img')  # 商标图片信息
                request_no = html.xpath('//tr[@class="ng-scope"][' + str(i) + ']/td[2]//text()')  # 申请/注册号
                world_type = html.xpath('//tr[@class="ng-scope"][' + str(i) + ']/td[3]//text()')  # 国际分类
                request_date = html.xpath('//tr[@class="ng-scope"][' + str(i) + ']/td[4]//text()')  # 申请日期
                mark_name = html.xpath('//tr[@class="ng-scope"][' + str(i) + ']/td[5]//text()')  # 商标名称
                request_name = html.xpath('//tr[@class="ng-scope"][' + str(i) + ']/td[6]//text()')  # 申请人（中文）
                item[request_no] = {'pic_url': pic_url, 'world_type': world_type, 'request_date': request_date, 'mark_name': mark_name, 'request_name': request_name}
                r.hset('huawei', mapping=item)
                item.clear()
            code = await page3.click('#mGrid_listGrid_paginator_0 > ul > li.nextPage > a')  # 点击下一页
            if code.status_code == 404:
                break
            await asyncio.sleep(15)

    except Exception as e:
        print(e)
        await browser.close()


if __name__ == '__main__':
    asyncio.run(run())
