# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class EbooksItem(scrapy.Item):
    # define the fields for your item here like:
    title = Field()
    desc = Field()
    image_urls = Field()
    author = Field()
    isbn = Field()
    year = Field()
    pages = Field()
    file_size = Field()
    file_format = Field()
    

    #House keeping field
    url = Field()
    project = Field()
    spider = Field()
    server = Field()
    date = Field()

