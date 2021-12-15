import random
import time

import requests
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def getDriver():
    options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--ignore-ssl-errors")
    # options.add_argument('--headless')  # 无界面形式
    options.add_argument('--user-agent=' + UserAgent().random)
    options.add_argument('--proxy-server={}'.format(get_proxies()))
    caps = DesiredCapabilities.CHROME.copy()
    caps['acceptInsecureCerts'] = True
    caps['acceptSslCerts'] = True
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"
    browser = webdriver.Chrome(options=options)
    with open('/home/wkun/Dev/python/work/stealth.min.js') as f:
        js = f.read()
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
    })
    browser.maximize_window()
    return browser


def get_proxies():
    ip_url = "http://192.168.10.25:8000/ip"
    proxies = requests.get(ip_url, headers={'User-Agent': 'Mozilla/5.0'}).json()
    proxy = proxies['https'].split('@')[-1]
    return proxy


def main():
    url = 'https://www.whoscored.com'
    driver = getDriver()
    driver.get(url)
    # html = driver.page_source
    # print(html)
    WebDriverWait(driver, 40).until(lambda x: x.find_element(By.XPATH, '//*[@class="divtable-row match"][1]/div[2]'))
    text = driver.find_element(By.XPATH, '//*[@class="divtable-row match"][1]/div[2]').get_attribute('textContent')
    print(text)
    page_1 = driver.current_window_handle
    li = [3, 4, 6, 7, 8, 9, 11]
    n = 1
    for i in li:
        WebDriverWait(driver, 40).until(lambda x: x.find_element(By.XPATH, '//*[@id="today"]/div/div[1]/div/div[' + str(i) + ']/div[9]/a[1]'))
        preview_url = driver.find_element(By.XPATH, '//*[@id="today"]/div/div[1]/div/div[' + str(i) + ']/div[9]/a[1]').get_attribute('href')
        new_tab = 'window.open("{}")'.format(preview_url)
        driver.execute_script(new_tab)
        handles = driver.window_handles
        driver.switch_to.window(driver.window_handles[n])
        WebDriverWait(driver, 40).until(lambda x: x.find_element(By.XPATH, '//*[@id="preview-lineups"]/div[1]/div[1]/div/a'))
        html = driver.find_element(By.XPATH, '//*[@id="preview-lineups"]/div[1]/div[1]/div/a').get_attribute('textContent')
        print(html)
        n += 1
        driver.switch_to.window(driver.window_handles[0])


if __name__ == "__main__":
    main()
