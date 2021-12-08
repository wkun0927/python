# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-11-23 10:37:52
# @Descripttion:

import json
import random
import re
import string
import time

import cv2 as cv
import pysnooper
import pytesseract
import redis
import requests
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from user_agent import generate_user_agent


def getDriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--headless')  # 无界面形式
    options.add_argument('--no-sandbox')  # 取消沙盒模式
    options.add_argument('--disable-setuid-sandbox')
    # options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--incognito')  # 启动进入隐身模式
    options.add_argument('--lang=zh-CN')  # 设置语言为简体中文
    options.add_argument('--user-agent=' + generate_user_agent())
    options.add_argument('--hide-scrollbars')
    options.add_argument('--disable-bundled-ppapi-flash')
    options.add_argument('--mute-audio')
    # options.add_argument('--proxy-server={}'.format(get_proxies()))
    browser = webdriver.Chrome(options=options)
    browser.set_window_size(1920, 1080)
    browser.execute_cdp_cmd("Network.enable", {})
    browser.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {"source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => false
            })
        """})

    return browser


def get_verification_code(email):
    # 请求邮箱API获取验证码
    proxies = get_proxies()
    for i in range(50):
        try:
            req = requests.get('https://snapmail.cc/emailList/' + email, proxies=proxies, timeout=3)  # https://snapmail.cc/emailList/delespider1@snapmail.cc
        except Exception:
            continue
        if req.status_code == 200:
            email_text = json.loads(req.text)[0]['html']
            validation_code = re.search(r'([0-9]{4})', email_text)
            return validation_code.group(1)
        time.sleep(3)


def get_proxies():
    ip_url = "http://192.168.10.25:8000/ip"
    proxies = requests.get(ip_url, headers={'User-Agent': 'Mozilla/5.0'}).json()
    return proxies['http']


def create_phone():
    # 随机手机号
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


def write_account_group_name(r):
    # 想redis中写入注册的帐号和cookie的组的名字
    group = dict()
    for i in range(1, 6):
        group['account_group' + str(i)] = 'cookie_group' + str(i)
        r.hset('account_group_names', mapping=group)
        r.set('index', 0)
    return 0


class ValidationCodeIsNoneError(Exception):
    pass


def register(r, account_name):
    # 注册帐号
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"
    userinfo = dict()
    email_num_path = '/home/wkun/Dev/python/work/patent/data/email_num.json'
    # url = 'http://123.233.113.66:8060/'
    url = 'http://60.166.52.165:8030/'
    name_A = string.ascii_uppercase
    name_a = string.ascii_lowercase
    name_n = string.digits
    name_t = '!@~`*$%^&'
    driver = getDriver()
    driver.get(url)
    WebDriverWait(driver, 15).until(lambda x: x.find_element(By.XPATH, '//div[2]/div/div[3]/div[1]/a[1]'))
    driver.find_element(By.XPATH, '//div[2]/div/div[3]/div[1]/a[1]').click()  # 同意
    with open(email_num_path) as x:  # 注册邮箱序号
        num = json.load(x)
    min_num = num[0]
    max_num = num[1]
    while min_num <= max_num:
        driver.get(url)
        try:
            time.sleep(5)
            email = 'berujo' + str(min_num) + '@snapmail.cc'  # 邮箱
            print(email)
            # email = 'hanne@snapmail.cc'
            username_n = random.randint(4, 19)
            password_n = random.randint(12, 19)
            username_l = []
            password_l = []
            username_n = random.randint(4, 19)
            for i_1 in range(username_n // 2):
                username_l.append(random.choice(string.ascii_letters))
            for i_2 in range(username_n // 2, username_n):
                username_l.append(random.choice(name_n))
            if random.randint(0, 1) == 1:
                index = random.randint(1, len(username_l))
                username_l.insert(index, '_')
            username = ''.join(username_l)  # 用户名

            for j_1 in range(password_n // 4 * 1):
                password_l.append(random.choice(name_A))
            for j_2 in range(password_n // 4 * 1, password_n // 4 * 2):
                password_l.append(random.choice(name_a))
            for j_3 in range(password_n // 4 * 2, password_n // 4 * 3):
                password_l.append(random.choice(name_n))
            for j_4 in range(password_n // 4 * 3, password_n):
                password_l.append(random.choice(name_t))
            password = ''.join(password_l)  # 密码

            WebDriverWait(driver, 15).until(lambda x: x.find_element(By.XPATH, '//*[@id="globleBody"]/div[2]/div[1]/div[3]/div[2]/div[2]/a[2]'))
            driver.find_element(By.XPATH, '//*[@id="globleBody"]/div[2]/div[1]/div[3]/div[2]/div[2]/a[2]').click()  # 点击“注册”
            WebDriverWait(driver, 15).until(lambda x: x.find_element(By.XPATH, '//input[@name="userAccount.account.username"]'))
            driver.find_element(By.XPATH, '//input[@name="userAccount.account.username"]').send_keys(username)  # 用户名
            driver.find_element(By.XPATH, '//input[@name="userAccount.account.password"]').send_keys(password)  # 密码
            driver.find_element(By.XPATH, '//*[@id="recheckPwd"]/label/div[1]/input').send_keys(password)  # 确认密码
            try:
                mes = driver.find_element(By.XPATH, '//*[@id="password"]/label/div[2]/span[2]').get_attribute('textContent')
                if mes:
                    continue
            except AttributeError:
                pass
            driver.find_element(By.XPATH, '//*[@id="email"]/label/div[1]/input').send_keys(email)  # 邮箱
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="emailCode"]/label/div[2]/a').click()  # 点击发送验证码
            time.sleep(1)
            check_email = driver.find_element(By.XPATH, '//*[@id="email"]/label/div[2]/span[2]').get_attribute('textContent')
            if check_email == '邮箱名已存在':
                min_num += 1
                continue
            num = time.time()
            x = 0
            while True:
                info = driver.find_element(By.XPATH, '//*[@id="emailCode"]/label/div[2]/span[2]').get_attribute('textContent')
                if info == '验证码发送成功':
                    validation_code = get_verification_code(email)  # 获取验证码
                    print(validation_code)
                    if validation_code is None:
                        x += 1
                        if x <= 5:
                            continue
                        else:
                            raise ValidationCodeIsNoneError('validation_code is none!')
                    break
                else:
                    if time.time() - num >= 120 or info == '验证码发送失败':
                        driver.find_element(By.XPATH, '//*[@id="emailCode"]/label/div[2]/a').click()  # 点击发送验证码

            driver.find_element(By.XPATH, '//*[@id="emailCode"]/label/div[1]/input').send_keys(validation_code)  # 输入验证码
            info = driver.find_element(By.XPATH, '//*[@id="emailCode"]/label/div[2]/span[2]').get_attribute('textContent')
            if info == '邮箱验证码输入错误':
                continue

            driver.find_element(By.XPATH, '//*[@id="mobile"]/label/div[1]/input').send_keys(create_phone())  # 输入随机手机号
            # driver.find_element(By.XPATH, '//*[@id="higherArea"]/option[' + str(random.randint(2, 35)) + ']').click()  # 随机点击省份
            driver.implicitly_wait(1)
            count = 2
            sel = []
            while True:
                try:
                    con = driver.find_element(By.XPATH, '//*[@id="province"]/option[' + str(count) + ']').get_attribute('value')
                    sel.append(con)
                    count += 1
                except NoSuchElementException:
                    break

            while True:
                try:
                    driver.find_element(By.XPATH, '//*[@id="province"]/option[@value="' + random.choice(sel) + '"]').click()  # 随机市区
                    break
                except NoSuchElementException:
                    continue
            driver.implicitly_wait(1)
            driver.find_element(By.XPATH, '//*[@id="company_catalog"]/option[@value="' + str(random.randint(1, 13)) + '"]').click()  # 用户类别
            driver.implicitly_wait(1)
            driver.find_element(By.XPATH, '//*[@id="agreement"]/div/p/label/input').click()  # 我已经阅读并同意
            driver.find_element(By.XPATH, '//*[@id="regBtn"]/label/div/a').click()  # 立即注册
            time.sleep(3)
            min_num += 1
            userinfo[username] = password
        except ValidationCodeIsNoneError:
            min_num += 1
            continue
        except Exception:
            continue
    r.hset(account_name, mapping=userinfo)
    userinfo.clear()
    # json_data = json.dumps(userinfo)
    # with open('./data/总网站.json', 'a') as f:
    #     f.write(json_data)
    num = [min_num, max_num + 10]
    with open(email_num_path, 'w') as s:
        json.dump(num, s)


def recognize_text(image, img_path):
    # 识别验证码图片
    # 打开文件夹中的图片
    image = Image.open(img_path)
    # 灰度图
    lim = image.convert('L')
    # 灰度阈值设为165，低于这个值的点全部填白色
    threshold = 150
    table = []

    for j in range(256):
        if j < threshold:
            table.append(0)
        else:
            table.append(1)

    bim = lim.point(table, '1')
    bim.save(img_path)
    text = pytesseract.image_to_string(bim)
    text = re.findall('\d+', text)
    text = ''.join(text)
    return text


def get_cookie(r, cookie_group_name, account_name):
    cookie = dict()
    img_full_path = '/home/wkun/Dev/python/work/patent/img/full.png'
    img_cut_path = '/home/wkun/Dev/python/work/patent/img/cut.png'
    url = 'http://60.166.52.165:8030/pubsearch/portal/uilogin-forwardLogin.shtml'
    pairs = r.hgetall(account_name)
    userinfo = dict()
    for key, value in pairs.items():
        key = str(key, encoding="utf-8")
        value = str(value, encoding="utf-8")
        userinfo[key] = value

    for username in userinfo.keys():
        password = userinfo[username]
        driver = getDriver()
        while True:
            driver.get(url)
            try:
                WebDriverWait(driver, 5).until(lambda x: x.find_element(By.XPATH, '//*[@id="j_username"]'))
            except Exception:
                continue
            name = driver.find_element(By.XPATH, '//*[@id="j_username"]')
            name.click()
            time.sleep(1)
            name.send_keys(username)  # 输入用户名
            word = driver.find_element(By.XPATH, '//*[@id="j_password_show"]')
            word.click()
            time.sleep(1)
            word.send_keys(password)  # 输入用户密码

            # 截图识别验证码
            img = driver.find_element(By.XPATH, '//*[@id="codePic"]')
            driver.save_screenshot(img_full_path)
            left = img.location['x']
            top = img.location['y']
            right = img.location['x'] + img.size['width']
            bottom = img.location['y'] + img.size['height']
            im = Image.open(img_full_path)
            im = im.crop((left, top, right, bottom))
            im.save(img_cut_path)
            src = cv.imread(img_cut_path)
            text = recognize_text(src, img_cut_path)
            driver.find_element(By.XPATH, '//*[@id="j_validation_code"]').send_keys(text)  # 输入验证码
            driver.find_element(By.XPATH, '//*[@id="loginForm"]/div[5]/a').click()  # 点击登陆
            time.sleep(1)
            try:
                # 是否有输入错误，有则重新开始，无则跳过。
                mes = driver.find_element(By.XPATH, '//*[@i="content"]').get_attribute('textContent')
                if mes == '验证码错误！Verification Code Error!':
                    # driver.find_element(By.XPATH, '//*[@type="button"]').click()
                    # driver.find_element(By.XPATH, '//*[@id="j_username"]').clear()
                    # driver.find_element(By.XPATH, '//*[@id="j_password_show"]').clear()
                    # driver.find_element(By.XPATH, '//*[@id="j_validation_code"]').clear()
                    # driver.find_element(By.XPATH, '//*[@id="codePic"]').click()
                    continue
                elif mes == '登录失败次数超过6次，帐号锁定，30分钟内不能登录':
                    n = 1
                    break
                elif mes == '用户名或密码错误！ Username or password error!':
                    n = 2
                    break
            except NoSuchElementException:
                n = 0
                break
            except Exception as e:
                n = 0
                print(e)
                break

        if n == 1:
            continue
        elif n == 2:
            r.hdel(cookie_group_name, username)
            driver.quit()
            continue
        time.sleep(5)
        try:
            pingbi = driver.find_element(By.XPATH, '//div/div/div/div[1]/div/p/span').get_attribute('textContent')
            if pingbi == '您当前访问的用户名已被屏蔽，请联系管理员。':
                r.hdel(cookie_group_name, username)
                continue
        except Exception:
            pass
        cookies = driver.get_cookies()
        JSESSIONID = cookies[-1]['value']
        cookie[username] = JSESSIONID
        time.sleep(1)
        driver.quit()
    r.hset(cookie_group_name, mapping=cookie)


def main():
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    write_account_group_name(r)
    pairs = r.hgetall('account_group_names')
    for key, value in pairs.items():
        account = str(key, encoding="utf-8")
        cookie_name = str(value, encoding="utf-8")
        register(r, account)
        get_cookie(r, cookie_name, account)


if __name__ == "__main__":
    main()
