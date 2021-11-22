#! user/bin/env python
# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-08-25 11:18:57
# @LastEditors: 王琨
# @LastEditTime: 2021-08-25 11:19:50
# @FilePath: /python/工作内容/税务/qinghau_req.py
# @Description: 

import requests
from user_agent import generate_user_agent

cookies = {
    'yfx_c_g_u_id_10003705': '_ck21082511031912780275474275377',
    'yfx_f_l_v_t_10003705': 'f_t_1629860599274__r_t_1629860599274__v_t_1629860599274__r_c_0',
}

headers = {
    'user-agent': generate_user_agent()
}

response = requests.get('http://qinghai.chinatax.gov.cn/web/qhswfaj/201907/d0896393e67548d29d17a9b85b082dc6.shtml', headers=headers, verify=False)
print(response.text)
