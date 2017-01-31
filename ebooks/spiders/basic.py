# -*- coding: utf-8 -*-
import socket
import datetime
import scrapy
from urllib.parse import urljoin
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join, TakeFirst
from scrapy.http.request import Request
from ebooks.items import EbooksItem


class BasicSpider(scrapy.Spider):
    name = "basic"
    allowed_domains = ["allitebooks.com"]
    #start_urls = ['http://www.allitebooks.com/']

    def start_requests(self):
        pages = 2 # total pagination in this site
        base_url = 'http://www.allitebooks.com'
        for p in range(2, pages + 1):
            yield scrapy.Request(urljoin(base_url, '/page/'+ str(p)), 
                callback=self.parse)


    def parse(self, response):
        detail_links = response.xpath('//h2/a/@href').extract()
        for details in detail_links:
            yield scrapy.Request(details, callback=self.parse_item)


    def parse_item(self, response):
        l = ItemLoader(item=EbooksItem(), response=response)
        #l.default_output_processor = TakeFirst()

        l.add_xpath('title', '//*[@class="single-title"][1]/text()')
        l.add_xpath('desc', '//*[@class="entry-content"][1]//text()', Join())
        #l.add_xpath('file_urls', '//*[@class="download-links"][1]/a/@href')
        #l.add_xpath('image_urls', '//*[contains(@class,"attachment-post-thumbnail")][1]/@src')
        
        #book details
        l.add_xpath('author', '//*[@class="book-detail"][1]/dl/dd[1]/a//text()')
        l.add_xpath('isbn', '//*[@class="book-detail"][1]/dl/dd[2]/text()')
        l.add_xpath('year', '//*[@class="book-detail"][1]/dl/dd[3]/text()',
            MapCompose(lambda i: i.strip(), int))
        l.add_xpath('pages', '//*[@class="book-detail"][1]/dl/dd[4]/text()',
            MapCompose(lambda i: i.strip(), int))
        l.add_xpath('file_size', '//*[@class="book-detail"][1]/dl/dd[6]/text()',
            MapCompose(self.parse_filesize, int))
        l.add_xpath('file_format', '//*[@class="book-detail"][1]/dl/dd[7]/text()')


        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())

        return l.load_item()


    def parse_filesize(self, value):
        result = 0
        try:
            postfix = value.strip().split(' ')[-1]
            factor = 1
            if postfix.strip().upper() == 'MB':
                factor = 1000000
            elif postfix.strip().upper() == 'GB':
                factor = 1000000000
            result = float(value.strip().split(' ')[0]) * factor
        except:
            result = 0

        return result


