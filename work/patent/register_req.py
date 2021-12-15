# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-10-21 10:58:32
# @Descripttion:

import base64
import json
import random
import re
import string
import time

import pysnooper
import requests
from readability import Document


def get_proxies():
    ip_url = "http://152.136.208.143:5000/w/ip/random"
    proxies = requests.get(ip_url, headers={'User-Agent': 'Mozilla/5.0'}).json()
    print(proxies['http'])
    return proxies['http']


def get_verification_code():
    for i in range(50):
        req = requests.get('https://www.snapmail.cc/emailList/bikp@snapmail.cc?isPrefix=True&count=1')
        if req.status_code == 200:
            email_text = json.loads(req.text)[0]['html']
            validation_code = re.search(r'([0-9]{4})', email_text)
            return validation_code.group(1)

        print("Waiting for next retry")
        time.sleep(6)


def create_phone():
    # 第二位数字
    second = [3, 4, 5, 7, 8][random.randint(0, 4)]

    # 第三位数字
    third = {
        3: random.randint(0, 9),
        4: [5, 7, 9][random.randint(0, 2)],
        5: [i for i in range(10) if i != 4][random.randint(0, 8)],
        7: [i for i in range(10) if i not in [4, 9]][random.randint(0, 7)],
        8: random.randint(0, 9),
    }[second]

    # 最后八位数字
    suffix = random.randint(9999999, 100000000)

    # 拼接手机号
    return "1{}{}{}".format(second, third, suffix)


def create_username():
    username_n = random.randint(4, 19)
    username_l = []
    for i_1 in range(username_n):
        username_l.append(random.choice(string.ascii_letters + string.digits))
    if random.randint(0, 1) == 1:
        index = random.randint(0, len(username_l))
        username_l.insert(index, '_')
    username = ''.join(username_l)  # 用户名
    return username


def create_passwd():
    char_A = string.ascii_uppercase
    char_a = string.ascii_lowercase
    char_n = string.digits
    char_t = '~!@#$%^&*()_+=.-'
    password_n = random.randint(12, 19)
    password_l = []
    for j in range(password_n):
        password_l.append(random.choice(char_A + char_a + char_n + char_t))
    password = ''.join(password_l)  # 密码
    return password


# 主函数
@pysnooper.snoop('./Log/file.log')
def main():
    userinfo = dict()
    code = 0
    for i in range(100):
        password = create_passwd()
        # email = 'kiufaku' + str(i + 1) + '@snapmail.cc'  # 邮箱
        email = 'bikp@snapmail.cc'

        # 请求头
        headers = {
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'http://123.233.113.66:8060',
            'Referer': 'http://123.233.113.66:8060/pubsearch/portal/uiregister-showRegisterPage.shtml',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        }

        # 省份代码
        province_select = ['110000', '120000', '130000', '140000', '150000', '210000', '220000', '230000', '310000', '320000', '330000', '340000', '350000', '360000', '370000', '410000', '420000', '430000', '440000', '450000', '460000', '500000', '510000', '520000', '530000', '540000', '610000', '620000', '630000', '640000', '650000', '710000', ' 810000', '820000']

        # data信息
        email_name = {
            'email': email
        }
        procince_code = random.choice(province_select)
        areaCode = {
            'areaCode': procince_code
        }

        # IP代理
        proxies = {
            'http': get_proxies()
        }

        # url信息
        preExecuteSearch = 'http://123.233.113.66:8060/pubsearch/patentsearch/preExecuteSearch!preExecuteSearch.do'
        username_url = 'http://123.233.113.66:8060/pubsearch/portal/uiregister-checkUserName.shtml'
        check_email_url = 'http://123.233.113.66:8060/pubsearch/portal/uiregister-checkEmailIsExist.shtml'
        generateEmailCode_url = 'http://123.233.113.66:8060/pubsearch/portal/uiregister-generateEmailCode.shtml'
        check_emailcode_url = 'http://123.233.113.66:8060/pubsearch/portal/uiregister-checkEmailCode.shtml'
        province_url = 'http://123.233.113.66:8060/pubsearch/portal/uiregister-showCity.shtml'
        register_url = 'http://123.233.113.66:8060/pubsearch/portal/uiregisterAC!register.do'

        s = requests.session()
        s.proxies = proxies
        cookies = s.post(url=preExecuteSearch, headers=headers, verify=False)  # 得到cookies
        print(cookies.cookies, cookies.text)

        while True:
            username = create_username()
            data_username = {'userNameForCheck': username}
            name = s.post(url=username_url, data=data_username, headers=headers, verify=False)  # 检查用户名
            if name.json()['isExist'] == 'AlreadyExisted':
                continue
            else:
                break
        time.sleep(3)

        while True:
            mail = s.post(url=check_email_url, data=email_name, headers=headers, verify=False)  # 检查邮箱是否存在
            if mail.json()['isExistEmail'] == '1':
                continue
            elif mail.json()['isExistEmail'] is None:
                break
        time.sleep(3)

        while True:
            send = s.post(url=generateEmailCode_url, data=email_name, headers=headers, verify=False)  # 发送验证码
            info = send.json()['sendSuccess']
            if send.json()['sendSuccess'] == 'false':
                time.sleep(120)
                continue
            else:
                break
        time.sleep(3)

        # 获取验证码，检查验证码是否最新
        while True:
            validation_code = get_verification_code()
            if validation_code != code:
                code = validation_code
                break
            else:
                time.sleep(5)
            time.sleep(3)

        # 将验证码加入到data中
        email_code = {
            'validateEmailCode': validation_code
        }

        while True:
            code = s.post(url=check_emailcode_url, data=email_code, headers=headers, verify=False)  # 网页检查验证码
            if code.json()['validateEmailCodeFlag'] == 'false':
                continue
            else:
                break
        time.sleep(3)

        area_list = s.post(url=province_url, data=areaCode, headers=headers, verify=False)  # 选择省
        city_list = []
        for n in area_list.json()['areaCodeList']:
            city_list.append(n['code'])

        city_value = random.choice(city_list)

        # base64编码
        en_username = str(base64.b64encode(username.encode('utf-8')))
        en_password = str(base64.b64encode(password.encode("utf-8")))
        en_email = str(base64.b64encode(email.encode("utf-8")))
        en_phone = str(base64.b64encode(create_phone().encode("utf-8")))

        data = {
            '------WebKitFormBoundary6HhRcdlCDDznl1Nd\r\nContent-Disposition: form-data; name': '"afterRegUrl"\r\n\r\n\r\n------WebKitFormBoundary6HhRcdlCDDznl1Nd\r\nContent-Disposition: form-data; name="wee.bizlog.modulelevel"\r\n\r\n0101402\r\n------WebKitFormBoundary6HhRcdlCDDznl1Nd\r\nContent-Disposition: form-data; name="validateEmailCode"\r\n\r\n' + validation_code + '\r\n------WebKitFormBoundary6HhRcdlCDDznl1Nd\r\nContent-Disposition: form-data; name="userAccount.user.extendInfo.highArea"\r\n\r\nCN\r\n------WebKitFormBoundary6HhRcdlCDDznl1Nd\r\nContent-Disposition: form-data; name="userAccount.user.extendInfo.area_id"\r\n\r\n' + city_value + '\r\n------WebKitFormBoundary6HhRcdlCDDznl1Nd\r\nContent-Disposition: form-data; name="userAccount.user.extendInfo.province"\r\n\r\n' + procince_code + '\r\n------WebKitFormBoundary6HhRcdlCDDznl1Nd\r\nContent-Disposition: form-data; name="userAccount.user.description"\r\n\r\n' + str(random.randint(1, 13)) + '\r\n------WebKitFormBoundary6HhRcdlCDDznl1Nd\r\nContent-Disposition: form-data; name="userAccount.AdvanceUserInfo.info_status"\r\n\r\n0\r\n------WebKitFormBoundary6HhRcdlCDDznl1Nd\r\nContent-Disposition: form-data; name="file"; filename=""\r\nContent-Type: application/octet-stream\r\n\r\n\r\n------WebKitFormBoundary6HhRcdlCDDznl1Nd\r\nContent-Disposition: form-data; name="fileName"\r\n\r\n\r\n------WebKitFormBoundary6HhRcdlCDDznl1Nd\r\nContent-Disposition: form-data; name="userAccount.AdvanceUserInfo.policy"\r\n\r\n\r\n------WebKitFormBoundary6HhRcdlCDDznl1Nd\r\nContent-Disposition: form-data; name="userAccount.AdvanceUserInfo.company_brief"\r\n\r\n\r\n------WebKitFormBoundary6HhRcdlCDDznl1Nd\r\nContent-Disposition: form-data; name="userAccount.account.username"\r\n\r\n' + en_username + '\r\n------WebKitFormBoundary6HhRcdlCDDznl1Nd\r\nContent-Disposition: form-data; name="userAccount.account.password"\r\n\r\n' + en_password + '\r\n------WebKitFormBoundary6HhRcdlCDDznl1Nd\r\nContent-Disposition: form-data; name="userAccount.user.email"\r\n\r\n' + en_email + '\r\n------WebKitFormBoundary6HhRcdlCDDznl1Nd\r\nContent-Disposition: form-data; name="userAccount.user.extendInfo.mobile"\r\n\r\n' + en_phone + '\r\n------WebKitFormBoundary6HhRcdlCDDznl1Nd\r\nContent-Disposition: form-data; name="userAccount.AdvanceUserInfo.company_name"\r\n\r\n\r\n------WebKitFormBoundary6HhRcdlCDDznl1Nd\r\nContent-Disposition: form-data; name="userAccount.AdvanceUserInfo.company_code"\r\n\r\n\r\n------WebKitFormBoundary6HhRcdlCDDznl1Nd\r\nContent-Disposition: form-data; name="userAccount.AdvanceUserInfo.company_owner"\r\n\r\n\r\n------WebKitFormBoundary6HhRcdlCDDznl1Nd\r\nContent-Disposition: form-data; name="userAccount.AdvanceUserInfo.register_date"\r\n\r\n\r\n------WebKitFormBoundary6HhRcdlCDDznl1Nd\r\nContent-Disposition: form-data; name="userAccount.AdvanceUserInfo.applicant_name"\r\n\r\n\r\n------WebKitFormBoundary6HhRcdlCDDznl1Nd\r\nContent-Disposition: form-data; name="userAccount.AdvanceUserInfo.applicant_title"\r\n\r\n\r\n------WebKitFormBoundary6HhRcdlCDDznl1Nd\r\nContent-Disposition: form-data; name="userAccount.AdvanceUserInfo.company_tel"\r\n\r\n\r\n------WebKitFormBoundary6HhRcdlCDDznl1Nd\r\nContent-Disposition: form-data; name="userAccount.AdvanceUserInfo.company_fax"\r\n\r\n\r\n------WebKitFormBoundary6HhRcdlCDDznl1Nd\r\nContent-Disposition: form-data; name="userAccount.AdvanceUserInfo.company_address"\r\n\r\n\r\n------WebKitFormBoundary6HhRcdlCDDznl1Nd\r\nContent-Disposition: form-data; name="userAccount.AdvanceUserInfo.company_zipcode"\r\n\r\n\r\n------WebKitFormBoundary6HhRcdlCDDznl1Nd\r\nContent-Disposition: form-data; name="userAccount.AdvanceUserInfo.apply_reason"\r\n\r\n\r\n------WebKitFormBoundary6HhRcdlCDDznl1Nd--'
        }

        final_headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Origin': 'http://123.233.113.66:8060',
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary6HhRcdlCDDznl1Nd',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': 'http://123.233.113.66:8060/pubsearch/portal/uiregister-showRegisterPage.shtml',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        }
        base_headers = {
            'Connection': 'keep-alive',
            'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://123.233.113.66:8060/pubsearch/portal/uiregister-showRegisterPage.shtml',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        }

        s.post(url=username_url, data=data_username, headers=headers, verify=False)
        s.post(url=check_email_url, data=email_name, headers=headers, verify=False)
        s.post(url=check_emailcode_url, data=email_code, headers=headers, verify=False)
        html = s.post(url=register_url, data=data, headers=final_headers, verify=False)
        res = html.text
        print(res)
        doc = Document(html.text)
        result = doc.title()
        if result == '注册成功':
            userinfo[username] = password
            json_data = json.dumps(userinfo)
            with open('./data/userinfo.json', 'w') as f:
                f.write(json_data)
        time.sleep(10)
        break


if __name__ == "__main__":
    main()
