# -*- coding: utf-8 -*-
# @Author: wangkun
# @Date: 2021-12-02 13:52:19
# @Descripttion:

import json
import time
from multiprocessing import Process

import requests
from requests.adapters import HTTPAdapter


def main():
    record = dict()
    for i in range(200):
        address = {
            'address': '北京市海淀区北坞村路23号北坞创新园北区5号楼3001室'
        }
        response = requests.post(url='http://192.168.10.25:8983/amap', json=address)
        data = json.loads(response.text)
        # print(data)
        longitude = data.get('longitude')
        latitude = data.get('latitude')
        reg_address = data.get('reg_address')
        record['reg_address'] = reg_address
        record['longitude'] = longitude
        record['latitude'] = latitude
        print(len(record))


if __name__ == "__main__":
    process_list = []
    for i in range(500):
        p = Process(target=main)
        p.start()
        process_list.append(p)
    for p in process_list:
        p.join()
