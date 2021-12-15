#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-09-18 15:21:46
# @Description: 

# 请求服务器上的蓝图进行测试
import requests
import pysnooper


def send_post_image_nsfw(img1_path, url):
    """
    :param img1:
    :return:
    """
    files = {
        'img_path': open(img1_path, 'rb').read()
    }
    html = requests.post(url, files=files).text
    return html


@pysnooper.snoop()
def get():
    url = 'http://192.168.3.77:8991/yidun'
    path = './验证码图片/jiangsu_identifier.jpg'
    html = send_post_image_nsfw(path, url)
    return html


if __name__ == '__main__':
    a = get()
    a = eval(a)
    print(a, type(a))
