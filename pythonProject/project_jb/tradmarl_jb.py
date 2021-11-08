# -*- coding: utf-8 -*
# @Author: 王琨
# @Date: 2021-08-16 11:31:16
# @LastEditors: 王琨
# @LastEditTime: 2021-08-19 10:58:23
# @FilePath: /pythonProject/project_jb/tradmarl_jb.py
# @Description: 商标网多进程运行脚本

import os
from multiprocessing import Process


def main():
    os.system('python3 /home/kerwin/Dev/python/pythonProject/Tradmark_Check_pyp.py')


if __name__ == '__main__':
    process_list = []
    for i in range(5):
        p = Process(target=main)
        p.start()
        process_list.append(p)

    for p in process_list:
        p.join()
