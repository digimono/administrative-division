# -*- coding: utf-8 -*-

import logging

from scrapy.exceptions import CloseSpider
from scrapy.spiders import Spider

from administrative_division.items import AdmItem

logger = logging.getLogger(__name__)


class ZxAdmSpider(Spider):
    name = 'zx_adm_spider'
    allowed_domains = ['zxinc.org']
    start_urls = ['http://www.zxinc.org/gb2260-latest.htm']

    def parse(self, response):
        areas = response.xpath('/html/body/div/div/areacode/text()').extract()

        if len(areas) == 0:
            logger.warning('Area data crawl failed')
            raise CloseSpider('Area data crawl failed')

        for area in areas:
            content = area.replace('\r\n', '')
            if content == '':
                continue
            else:
                item = AdmItem()
                item['area'] = content
                yield item
