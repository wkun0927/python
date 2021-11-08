# -*- coding: utf-8 -*
# @Author: 王琨
# @Date: 2021-08-09 20:39:37
# @LastEditors: 王琨
# @LastEditTime: 2021-08-19 10:57:40
# @FilePath: /pythonProject/d.py
# @Description:

import json
import random
import re
import time

import cv2 as cv
import pytesseract
import requests
# second = [3, 4, 5, 7, 8][random.randint(0, 4)]
#
# # 第三位数字
# third = {
#     3: random.randint(0, 9),
#     4: [5, 7, 9][random.randint(0, 2)],
#     5: [i for i in range(10) if i != 4][random.randint(0, 8)],
#     7: [i for i in range(10) if i not in [4, 9]][random.randint(0, 7)],
#     8: random.randint(0, 9),
# }[second]
#
# # 最后八位数字
from PIL import Image

# for i in range(50):
#     req = requests.get('https://snapmail.cc/emailList/doid@snapmail.cc')
#     print(req.status_code)
#     if req.status_code == 200:
#         email_text = json.loads(req.text)[0]['html']
#         validation_code = re.search(r'([0-9]{4})', email_text)
#         print(validation_code.group(1))

#     print("Waiting for next retry")
#     time.sleep(6)

# suffix = random.randint(9999999, 100000000)
#
# # 拼接手机号
# print("1{}{}{}".format(second, third, suffix))


def recognize_text(image):
    # 边缘保留滤波  去噪
    blur = cv.pyrMeanShiftFiltering(image, sp=8, sr=60)
    # 灰度图像
    gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
    # 二值化  设置阈值  自适应阈值的话 黄色的4会提取不出来
    ret, binary = cv.threshold(gray, 185, 255, cv.THRESH_BINARY_INV)
    # 逻辑运算  让背景为白色  字体为黑  便于识别
    cv.bitwise_not(binary, binary)
    # 识别
    test_message = Image.fromarray(binary)
    text = pytesseract.image_to_string(test_message)
    text = re.findall('\d+', text)
    text = ''.join(text)
    cv.imshow(blur)
    cv.imshow(gray)
    print(text)
    return text


if __name__ == "__main__":
    src = cv.imread(r'../../专利/data/cut.png')
    recognize_text(src)
