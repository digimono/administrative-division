# -*- coding: utf-8 -*-

import logging

from scrapy.exceptions import CloseSpider
from scrapy.spiders import Spider

from administrative_division.items import AdministrativeDivisionItem

logger = logging.getLogger(__name__)


class AdmSpider(Spider):
    name = "zx_administrative_division"
    allowed_domains = ["zxinc.org"]
    start_urls = ["http://www.zxinc.org/gb2260-latest.htm"]

    def parse(self, response):
        areas = response.xpath("/html/body/div/div/areacode/text()").extract()

        if len(areas) == 0:
            logger.warning("Area data crawl failed")
            raise CloseSpider("Area data crawl failed")

        for area in areas:
            content = area.replace("\r\n", "")
            if content == "":
                continue
            else:
                item = AdministrativeDivisionItem()
                item["area"] = content
                yield item
