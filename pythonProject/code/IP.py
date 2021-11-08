import requests


def get_proxies():
    ip_url = "http://152.136.208.143:5000/w/ip/random"
    proxies = requests.get(ip_url, headers={'User-Agent': 'Mozilla/5.0'}).json()
    return proxies


if __name__ == '__main__':
    a = get_proxies()
    print(a)
