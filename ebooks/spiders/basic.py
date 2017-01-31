# -*- coding: utf-8 -*-
import socket
import datetime
import scrapy
from urllib.parse import urljoin
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from scrapy.http.request import Request
from ebooks.items import EbooksItem


class BasicSpider(scrapy.Spider):
    name = "basic"
    allowed_domains = ["allitebooks.com"]
    #start_urls = ['http://www.allitebooks.com/']

    def start_requests(self):
        pages = 2 # total pagination in this site
        base_url = 'http://www.allitebooks.com'
        for p in range(1, pages + 1):
            yield scrapy.Request(urljoin(base_url, '/page/'+ str(p)), 
                callback=self.parse)


    def parse(self, response):
        detail_links = response.xpath('//h2/a/@href').extract()
        for details in detail_links:
            yield scrapy.Request(details, callback=self.parse_item)


    def parse_item(self, response):
        l = ItemLoader(item=EbooksItem(), response=response)
        #TODO: add processors
        l.add_xpath('title', '//*[@class="single-title"][1]/text()')

        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())

        return l.load_item()

