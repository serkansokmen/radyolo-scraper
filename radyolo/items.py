# -*- coding: utf-8 -*-
import scrapy


class StreamItem(scrapy.Item):
    username = scrapy.Field()
    text = scrapy.Field()
    timestamp = scrapy.Field()
