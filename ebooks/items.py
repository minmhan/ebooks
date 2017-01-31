# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field
from scrapy.loader.processors import TakeFirst


class EbooksItem(scrapy.Item):
    # define the fields for your item here like:
    title = Field(output_processor=TakeFirst())
    desc = Field(output_processor=TakeFirst())


    author = Field()
    isbn = Field(output_processor=TakeFirst())
    year = Field(output_processor=TakeFirst())
    pages = Field(output_processor=TakeFirst())
    file_size = Field(output_processor=TakeFirst())
    file_format = Field(output_processor=TakeFirst())

    image_urls = Field()
    images = Field(output_processor=TakeFirst())
    file_urls = Field()
    files = Field(output_processor=TakeFirst())


    #House keeping field
    url = Field(output_processor=TakeFirst())
    project = Field(output_processor=TakeFirst())
    spider = Field(output_processor=TakeFirst())
    server = Field(output_processor=TakeFirst())
    date = Field(output_processor=TakeFirst())

