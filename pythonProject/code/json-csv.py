# -*- coding: utf-8 -*
# @Author: 王琨
# @Date: 2021-08-16 13:59:29
# @LastEditors: 王琨
# @LastEditTime: 2021-08-16 14:03:23
# @FilePath: /pythonProject/json-csv.py
# @Description: 

import json
import csv

for i in range(7, 38):
    with open('./data/' + str(i) + '.json') as f:
        json_list = json.loads(f.read())
    for url in json_list:
        List = [url]
        with open('./data/' + str(i) + '.csv', 'a') as s:
            s_csv = csv.writer(s)
            s_csv.writerow(List)
