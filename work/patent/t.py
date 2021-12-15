# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-11-08 11:04:29
# @Descripttion:

import re

import pytesseract
from PIL import Image


# 二值化处理
def two_value():
    for i in range(100):
        # 打开文件夹中的图片
        image = Image.open('./img/' + str(i) + '.png')
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
        bim.save('./test/' + str(i) + 't.png')
        text = pytesseract.image_to_string(bim)
        text = re.findall('\d+', text)
        text = ''.join(text)
        print(text)
        return text


two_value()
