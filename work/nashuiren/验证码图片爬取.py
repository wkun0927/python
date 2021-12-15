# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-08-26 15:37:31
# @Description: 

import requests
import time
import requests
from user_agent import generate_user_agent


for i in range(1):
    headers = {
        'user-agent': generate_user_agent()
    }
    params = (
        ('time', str(int(time.time())*1000)),
    )
    url = 'https://wbjr.chongqing.chinatax.gov.cn/PortalWeb/pages/sscx/cx_nsrzg.html'
    res = requests.get(url=url, headers=headers, params=params)
    print(res.status_code)
    name = str(i) + '.jpg'
    with open('/home/kerwin/Dev/字母验证码/' + name, 'wb') as f:
        f.write(res.content)
    time.sleep(1)
