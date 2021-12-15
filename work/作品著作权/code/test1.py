#encoding=utf-8

import sys, os
import numpy as np
from PIL import Image, ImageDraw

# 二值数组
t2val = {}
ave1 = []
ave2 = []
number = 0


def twoValue(image, G):
    for y in range(0, image.size[1]):
        for x in range(0, image.size[0]):

            g = image.getpixel((x, y))
            if g > G:
                t2val[(x, y)] = 1
            else:
                t2val[(x, y)] = 0


def threshold(image, number):
    if number == 0:
        number = np.mean(image)
    ave1.clear()
    ave2.clear()
    for y in range(0, image.size[1]):
        for x in range(0, image.size[0]):
            g = image.getpixel((x, y))
            if g > number:
                ave1.append(g)
            else:
                ave2.append(g)
    ave(image, number)


def ave(image, number):
    number1 = np.mean(ave1)
    number2 = np.mean(ave2)
    if 2 * number > (number1 + number2) + 5:
        number = (number1 + number2) / 2
        threshold(image, number)
    elif 2 * number < (number1 + number2) - 5:
        number = (number1 + number2) / 2
        threshold(image, number)
    else:
        number = (number1 + number2) / 2
        twoValue(image, number)


def saveImage(filename, size):
    image = Image.new("1", size)
    draw = ImageDraw.Draw(image)

    for x in range(0, size[0]):
        for y in range(0, size[1]):
            draw.point((x, y), t2val[(x, y)])

    image.save(filename)


filepath = 'F:/PycharmProjects/CnkjProjects/zpzzq/images'
for filename in os.listdir(filepath):
    image = Image.open('F:/PycharmProjects/CnkjProjects/zpzzq/images/%s' % filename).convert("L")
    threshold(image, 0)
    saveImage('F:/PycharmProjects/CnkjProjects/zpzzq/image/%s' % filename, image.size)

