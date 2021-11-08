#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-09-10 17:41:09
# @Description: 百度百科查询

from urllib.parse import quote

import pysnooper
import requests
from lxml import etree
from user_agent import generate_user_agent


@pysnooper.snoop()
def query(cont):
    url = 'https://baike.baidu.com/item/' + quote(cont)

    headers = {
        'User-Agent': generate_user_agent()
    }
    response = requests.get(url=url, headers=headers)
    html = etree.HTML(response.text)
    introduction = html.xpath('//*[@class="lemma-summary"]//text()')
    name = html.xpath('//*[@class="basicInfo-item name"]/text()')
    value = html.xpath('//*[@class="basicInfo-item value"]/text()')

    return introduction, name, value


if __name__ == '__main__':
    content = '华为技术有限公司'
    result = query(content)
    print(result)
