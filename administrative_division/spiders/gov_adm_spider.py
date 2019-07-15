# -*- coding: utf-8 -*-

import logging

from scrapy import Request
from scrapy.exceptions import CloseSpider
from scrapy.spiders import Spider

from administrative_division.items import AdmItem
from administrative_division.util.time_util import Wait

logger = logging.getLogger(__name__)


class GovAdmSpider(Spider):
    name = 'gov_adm_spider'
    allowed_domains = ['stats.gov.cn']
    start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/index.html']

    def parse(self, response):
        links = response.css("table[class='provincetable'] tr[class='provincetr'] td a")

        if len(links) == 0:
            logger.warning('Provinces data crawl failed')
            raise CloseSpider('Provinces data crawl failed')

        for index, link in enumerate(links):
            # name = Selector(text=link.extract()).css('a::text').extract_first()
            # name = link.xpath('normalize-space()').extract_first()
            name = link.xpath('string()').extract_first()
            href = link.xpath('@href').extract_first()
            code = int('{:<06}'.format(href.replace('.html', '')))
            next_url = response.urljoin(href)

            # args = (str(index + 1).zfill(2), code, '{:\u3000<08}'.format(name), next_url)
            # logger.debug('Province #%s: code %d name %s, url %s' % args)

            item = AdmItem()
            item['code'] = code
            item['name'] = name
            item['level'] = 1
            yield item

            Wait.wait_seconds(0.5, 1.5)
            yield Request(next_url, meta={'item': item}, callback=self.parse_city)

    def parse_city(self, response):
        # item = response.meta['item']
        tr_list = response.css("table[class='citytable'] tr[class='citytr']")

        if len(tr_list) > 0:
            for index, tr in enumerate(tr_list):
                link1 = tr.xpath('./td[1]/a')
                link2 = tr.xpath('./td[2]/a')

                code = int(link1.xpath('string()').extract_first()[0:6])
                name = link2.xpath('string()').extract_first()
                href = link1.xpath('@href').extract_first()
                next_url = response.urljoin(href)

                # args = (str(index + 1).zfill(2), code, name, next_url)
                # logger.debug('City #%s: code %d name %s, url %s' % args)

                item = AdmItem()
                item['code'] = code
                item['name'] = name
                item['level'] = 2
                yield item

                Wait.wait_seconds(0.5, 1.5)
                yield Request(next_url, meta={'item': item}, callback=self.parse_county)

    def parse_county(self, response):
        tr_list = response.css("table[class='countytable'] tr[class='countytr']")

        if len(tr_list) > 0:
            for index, tr in enumerate(tr_list):
                link1 = tr.xpath('./td[1]/a')
                link2 = tr.xpath('./td[2]/a')

                skip = len(link1) == 0
                if skip:
                    continue

                code = int(link1.xpath('string()').extract_first()[0:6])
                name = link2.xpath('string()').extract_first()
                # href = link1.xpath('@href').extract_first()

                item = AdmItem()
                item['code'] = code
                item['name'] = name
                item['level'] = 3
                yield item
