#coding=gbk
import re
url_prefix='https://www.thepaper.cn/'
strs='< a href="newsDetail_forward_12483801" target = "_blank" > < fontcolor = "#00a5eb" > �ֽ� < / font > < font color = "#00a5eb" > ���� < / font > ��ϯ����������ʼ���TikTokCEO < / a >'

link=re.findall(r'href="[\s\S]*" target', strs)
# print(link)
url=url_prefix+str(link).split('"')[1]
print(url)
title = re.sub(u"\\<.*?\\>", "", strs)
title_m=title.replace(' ','')
print(title_m)

