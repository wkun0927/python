import csv
url_list = []
urls = csv.reader(open('../data/page_url.csv', encoding='utf-8'))
for url in urls:
    url_list.append(url)
print(len(url_list[0]))