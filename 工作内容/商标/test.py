#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 王琨
# @Date: 2021-11-11 10:50:16
# @Descripttion:

import requests

cookies = {
    'tmas_cookie': '2272.7689.15400.0000',
    'goN9uW4i0iKzS': '5mqBKOW2bB66lJpermYpZ4bYEBa.lTQX.F6ss2wcwzMgYJXqxW1De8u_CJbnUe1g9G8XYxYNE4cwTaf.jRi8slq',
    '018f9ebcc3834ce269': '786826691e14955a2d92a6be6b32c3b6',
    '_trs_uv': 'kvubl6m5_4693_23hk',
    '_va_ref': '%5B%22%22%2C%22%22%2C1636596984%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D',
    '_va_id': '1335a6c8df6cd68e.1636596984.1.1636597013.1636596984.',
    'goN9uW4i0iKzT': '533nuDCDWzWLqqqmekwiNbGmnIHZSNocXTE11_ta25SoZ7RjPafwJIxmt3H9YaS14lAKqZ1YbuL4yK5dp2gxsmvwrDFURSkcczlarFdiLw5Nv2IcZtbHojd2w1JNnDWILz4JNd8nUFrKW6u9QAadDwTqCmAvU30rhsdy.W84cuieKSq5lyy5YvnY2OID_6d9o9wJEHpx6ID7rakDpci8Q9dW8m6rVh6joopuazaVWnT7OJuTlnl_djOGbn7OPVvCuiNQf8vMDn2uf1xUVNw4aVr8JoUgqIYTP_7X5E0MvvZam._E2xQiUfbcKCBVoslQQmZqVacsmckY2JrSIyhBE7b',
    'JSESSIONID': '0000FV0C94iFjPKTlEoFeMoNnpe:1bm112rsm',
}

headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'http://wsgg.sbj.cnipa.gov.cn:9080',
    'Referer': 'http://wsgg.sbj.cnipa.gov.cn:9080/tmann/annInfoView/annSearch.html?annNum=1766',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

params = (
    ('O56fzBVE', '5JhKakBXZ9zJY6BZTAqkk6J2.A_nbD77ouNjpIsfhSeNgtZwo3qobN7SRiJSCWB.kCGA4yY4ZcA7lfTSTSPfnoIUS2Kde60T3yxlNW20czBuMJlsDiHmLKuAgirkwH7qxJQlR.hpsTXIUtnI4YM_KcHoQllf06tUwlE6YcU7KV4FA85_zio37DwhXapqdBANh041x7IWlBiYJaN6ZHGi2J1bVqQrGhO9mSFI3h3zW_ERTRZFkoC2L2Gb7._K50tM8jNWT7KZppm7.nbX4aTOYUy5A3OUxGun.q7FCcLL4ZuMUSlh3cPP2I35Lnn4EbyCrk3IkiEe8OrB3A2QQTWBDoiFvN3uxujOiTGI6LQnaW7gsZkeutD2PVcLvLMySzDx1'),
)

data = {
  'id': 'e48b92fb7cc1565e017ce4878c8e4117',
  'pageNum': '1',
  'flag': '1'
}

response = requests.post('http://wsgg.sbj.cnipa.gov.cn:9080/tmann/annInfoView/imageView.html', headers=headers, cookies=cookies, data=data, verify=False)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.post('http://wsgg.sbj.cnipa.gov.cn:9080/tmann/annInfoView/imageView.html?O56fzBVE=5JhKakBXZ9zJY6BZTAqkk6J2.A_nbD77ouNjpIsfhSeNgtZwo3qobN7SRiJSCWB.kCGA4yY4ZcA7lfTSTSPfnoIUS2Kde60T3yxlNW20czBuMJlsDiHmLKuAgirkwH7qxJQlR.hpsTXIUtnI4YM_KcHoQllf06tUwlE6YcU7KV4FA85_zio37DwhXapqdBANh041x7IWlBiYJaN6ZHGi2J1bVqQrGhO9mSFI3h3zW_ERTRZFkoC2L2Gb7._K50tM8jNWT7KZppm7.nbX4aTOYUy5A3OUxGun.q7FCcLL4ZuMUSlh3cPP2I35Lnn4EbyCrk3IkiEe8OrB3A2QQTWBDoiFvN3uxujOiTGI6LQnaW7gsZkeutD2PVcLvLMySzDx1', headers=headers, cookies=cookies, data=data, verify=False)
print(response, response.content.decode('utf-8'))
