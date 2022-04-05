import requests

cookies = {
    'Hm_lvt_e6d7fcd5956d54d11255d0dc15fad005': '1647316583',
    'HWWAFSESID': '8000973aceab174eaf',
    'HWWAFSESTIME': '1647316721751',
    'Qs_lvt_332253': '1647316741',
    'Hm_lpvt_e6d7fcd5956d54d11255d0dc15fad005': '1647323620',
    'Qs_pv_332253': '805770346499319900%2C598324031789508400%2C575262610778784640%2C1119589587898652300%2C726144938518539800',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

response = requests.get('http://www.51xiazai.cn/sort/14/', headers=headers, cookies=cookies, verify=False)
