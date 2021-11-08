import requests
import re

url = "http://checkip.dyndns.org"
proxies={'http':'127.0.0.1:****'}
theIP = requests.get(url,proxies=proxies).text

print("your IP Address is: ",  theIP)