# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-08-26 14:08:47
# @Description: 

import requests
import random
import time

for i in range(5000):
    if i % 100 == 0:
        time.sleep(2)
    url = 'https://etax.hebei.chinatax.gov.cn/wszx-web/captcha.jpg?' + str(random.random())
    res = requests.get(url)
    name = str(i) + '.jpg'
    with open('/home/kerwin/Dev/河北验证码图片/' + name, 'wb') as f:
        f.write(res.content)
