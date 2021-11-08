# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date:   2021-05-24 14:14:35
# @Last Modified by:   王琨
# @Last Modified time: 2021-06-16 17:45:30
# coding=utf-8
# 最后一位校验码判断
# a1 a2 a3 …… a14 a15
# gszch = '110108000000016'
gszch = input('请输入工商注册号（14位数字）：')
gszch_list = list(gszch)
# 初始为10
tem3 = 10
# a1到a14进行变化
tem1 = 10 + int(gszch_list[0])
tem2 = int(gszch_list[0]) * 2
for i in range(1, 14):
    tem1 = tem2 % 11 + int(gszch_list[i])
    x = tem1 % 10
    if x == 0:
        x = 10
    tem2 = x * 2
    # print(tem1, tem2)

p15 = tem2 % 11
a15 = 11 - p15
if a15 == 10:
    a15 = 0
# 输出最后一位校验码	2003-12-22	2003-12-22Z
print(a15)


