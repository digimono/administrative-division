# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AdmItem(scrapy.Item):
    area = scrapy.Field()
    code = scrapy.Field()
    name = scrapy.Field()
    level = scrapy.Field()
    first_letter = scrapy.Field()


class AdmExportItem(scrapy.Item):
    code = scrapy.Field()
    name = scrapy.Field()
    level = scrapy.Field()
    region = scrapy.Field()
    parent_code = scrapy.Field()
    first_letter = scrapy.Field()
