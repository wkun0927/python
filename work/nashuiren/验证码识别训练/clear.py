#!usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-08-26 16:24:47
# @LastEditors: 王琨
# @LastEditTime: 2021-09-02 14:09:40
# @FilePath: /python/工作内容/一般纳税人/验证码识别训练/clear.py
# @Description: 去除验证码噪点

from PIL import Image


def main():
    im = Image.open("/home/wk/Dev/image/1.png")

    for y in range(im.size[1]):
        for x in range(im.size[0]):
            pix = im.getpixel((x, y))
            print(pix)


if __name__ == '__main__':
    main()
