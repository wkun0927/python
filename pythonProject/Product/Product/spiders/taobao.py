from scrapy import Spider, Request
from urllib.parse import quote
from Product.items import ProductItem


class TaobaoSpider(Spider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com']
    start_urls = ['http://www.taobao.com/']

    def parse(self, response, **kwargs):
        pass
