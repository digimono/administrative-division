# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import logging
import os

from scrapy import signals
from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter

from administrative_division.enums import ChinaRegion
from administrative_division.helper import Helper
from administrative_division.items import AdmExportItem

logger = logging.getLogger(__name__)

exclude_names = ["市辖区", "县", "省直辖县级行政区划", "自治区直辖县级行政区划"]
# 直辖市
municipalities = [110000, 120000, 310000, 500000]
# 自治区
autonomous_regions = [150000, 450000, 540000, 640000, 650000]
# 特别行政区
special_administrative_regions = [810000, 820000]

CHINA_REGION = {
    # 华东地区
    310000: ChinaRegion.East, 320000: ChinaRegion.East, 330000: ChinaRegion.East,
    340000: ChinaRegion.East, 350000: ChinaRegion.East, 360000: ChinaRegion.East,
    370000: ChinaRegion.East,
    # 华南地区
    440000: ChinaRegion.South, 450000: ChinaRegion.South, 460000: ChinaRegion.South,
    # 华中地区
    410000: ChinaRegion.Central, 420000: ChinaRegion.Central, 430000: ChinaRegion.Central,
    # 华北地区
    110000: ChinaRegion.North, 120000: ChinaRegion.North, 130000: ChinaRegion.North,
    140000: ChinaRegion.North, 150000: ChinaRegion.North,
    # 西北地区
    610000: ChinaRegion.Northwest, 620000: ChinaRegion.Northwest, 630000: ChinaRegion.Northwest,
    640000: ChinaRegion.Northwest, 650000: ChinaRegion.Northwest,
    # 西南地区
    500000: ChinaRegion.Southwest, 510000: ChinaRegion.Southwest, 520000: ChinaRegion.Southwest,
    530000: ChinaRegion.Southwest, 540000: ChinaRegion.Southwest,
    # 东北地区
    210000: ChinaRegion.Northeast, 220000: ChinaRegion.Northeast, 230000: ChinaRegion.Northeast,
    # 台港澳地区
    710000: ChinaRegion.HK_MAC_TW, 810000: ChinaRegion.HK_MAC_TW, 820000: ChinaRegion.HK_MAC_TW
}


class AdmPipeline(object):
    sep = "\u3000"

    def process_item(self, item, spider):
        if "area" in item:
            it = item["area"]
            item.__delitem__("area")

            # counter = Counter(it)
            # item["level"] = counter[sep]
            item["level"] = it.count(self.sep)

            if it.startswith("000000"):
                item["code"] = 0
                item["name"] = "中国"
            else:
                arr = it.split(self.sep)
                item["code"] = int(arr[0])
                item["name"] = arr[len(arr) - 1]

        code = str(item["code"])
        if code != "0" and len(code) != 6:
            raise DropItem("Area data crawl failed")

        name = item["name"]

        if name == "澳门新城区":
            item["name"] = "新城区"

        if name.endswith("特别行政区"):
            # item["name"] = name[0: name.index("特别行政区")]
            pass

        return item


class AssemPipeline(object):
    def __init__(self):
        self.rawDict = {}
        self.provDict = {}
        self.cityDict = {}
        self.countyDict = {}

    def process_item(self, item, spider):
        code = item["code"]
        if code not in self.rawDict:
            self.rawDict[code] = dict(item)

        self.assem_province(code, item)
        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.assem_city()
        self.assem_county()

        # self.cityDict = dict(sorted(self.cityDict.items(), key=operator.itemgetter(0)))
        self.cityDict = dict(sorted(self.cityDict.items(), key=lambda kv: kv[0]))

        logger.info(json.dumps(self.provDict, ensure_ascii=False))
        logger.info(json.dumps(self.cityDict, ensure_ascii=False))
        logger.info(json.dumps(self.countyDict, ensure_ascii=False))

        file_prov_path = os.path.abspath('../dist/provinces.json')
        file_city_path = os.path.abspath('../dist/cities.json')
        file_county_path = os.path.abspath('../dist/counties.json')

        with open(file=file_prov_path, encoding='utf-8', mode='w') as json_file:
            json_file.truncate()
            json.dump(self.provDict, json_file, ensure_ascii=False, indent=2)

        with open(file=file_city_path, encoding='utf-8', mode='w') as json_file:
            json_file.truncate()
            json.dump(self.cityDict, json_file, ensure_ascii=False, indent=2)

        with open(file=file_county_path, encoding='utf-8', mode='w') as json_file:
            json_file.truncate()
            json.dump(self.countyDict, json_file, ensure_ascii=False, indent=2)

    def assem_province(self, code, item):
        if Helper.is_prov(code):
            province = dict(item)
            province["level"] = 1
            province["parent_code"] = 0

            if code in CHINA_REGION:
                kv = CHINA_REGION.get(code)
                province["region"] = kv.value
            else:
                province["region"] = 0

            province["children"] = []
            self.provDict[code] = province

    def assem_city(self):
        for code in list(self.rawDict.keys()):
            if not Helper.is_city(code) or code in self.cityDict:
                continue

            prov_code = int(str(code)[0:2] + "0000")
            province = self.provDict.get(prov_code)

            city = self.rawDict[code]
            city["level"] = 2
            city["parent_code"] = prov_code
            city["children"] = []

            if prov_code in municipalities and city["name"] in exclude_names:
                city["name"] = province["name"]

            if not city["name"] in exclude_names:
                children = province["children"]
                if not self.check_duplicate(children, city, "name"):
                    children.append(city)

            self.cityDict[code] = city

    def assem_county(self):
        for code in list(self.rawDict.keys()):
            if not Helper.is_county(code):
                continue

            prov_code = int(str(code)[0:2] + "0000")
            city_code = int(str(code)[0:4] + "00")

            if prov_code == 500000 and city_code == 500200:
                city_code = 500100

            province = self.provDict.get(prov_code)
            city = self.cityDict.get(city_code)

            county = self.rawDict[code]

            if prov_code not in municipalities:
                if city is None or city["name"] in exclude_names:
                    county["level"] = 2
                    county["parent_code"] = prov_code
                    province["children"].append(county)

                    self.cityDict[code] = county

                    if city is not None:
                        del self.cityDict[city_code]
                else:
                    if county["name"] in exclude_names:
                        pass
                    else:
                        county["level"] = 3
                        county["parent_code"] = city_code
                        city["children"].append(county)
            else:
                county["level"] = 3
                county["parent_code"] = city_code
                city["children"].append(county)

            self.countyDict[code] = county

    def check_duplicate(self, items, it, key):
        if len(items) == 0:
            return False

        for item in items:
            if item[key] == it[key]:
                return True

        return False


class CsvExportPipeline(object):

    def __init__(self):
        self.provDict = {}
        self.cityDict = {}
        self.city_names = []
        self.files = {}

        file_prov_path = os.path.abspath('../dist/provinces.csv')
        file_city_path = os.path.abspath('../dist/cities.csv')
        file_county_path = os.path.abspath('../dist/counties.csv')

        file_prov = open(file_prov_path, 'w+b')
        file_city = open(file_city_path, 'w+b')
        file_county = open(file_county_path, 'w+b')

        self.files[file_prov_path] = file_prov
        self.files[file_city_path] = file_city
        self.files[file_county_path] = file_county

        self.prov_exporter = CsvItemExporter(file_prov)
        self.city_exporter = CsvItemExporter(file_city)
        self.county_exporter = CsvItemExporter(file_county)

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.prov_exporter.start_exporting()
        self.city_exporter.start_exporting()
        self.county_exporter.start_exporting()

    def spider_closed(self, spider):
        self.prov_exporter.finish_exporting()
        self.city_exporter.finish_exporting()
        self.county_exporter.finish_exporting()

        for file in self.files.values():
            file.close()

    def process_item(self, item, spider):
        code = item["code"]
        export_item = AdmExportItem()
        export_item["code"] = code
        export_item["name"] = item["name"]

        self.export_province(code, export_item)
        self.export_city(code, export_item)
        self.export_county(code, export_item)
        return item

    def export_province(self, code, item):
        if Helper.is_prov(code):
            self.provDict[code] = dict(item)

            item["level"] = 1
            item["parent_code"] = 0

            if code in CHINA_REGION:
                kv = CHINA_REGION.get(code)
                item["region"] = kv.value
            else:
                item["region"] = 0

            self.prov_exporter.export_item(item)

    def export_city(self, code, item):
        if Helper.is_city(code):
            if code in self.cityDict:
                return

            prov_code = int(str(code)[0:2] + "0000")
            item["level"] = 2
            item["parent_code"] = prov_code
            item["region"] = 0

            province = self.provDict.get(prov_code)
            if prov_code in municipalities:
                if item["name"] in exclude_names:
                    item["name"] = province["name"]

            p_name = str(item["parent_code"]) + ":" + item["name"]
            if p_name not in self.city_names:
                self.city_names.append(p_name)
                if not item["name"] in exclude_names:
                    self.city_exporter.export_item(item)

            self.cityDict[code] = dict(item)

    def export_county(self, code, item):
        if Helper.is_county(code):
            prov_code = int(str(code)[0:2] + "0000")
            city_code = int(str(code)[0:4] + "00")

            if prov_code == 500000 and city_code == 500200:
                city_code = 500100

            # province = self.provDict.get(prov_code)
            city = self.cityDict.get(city_code)

            item["region"] = 0

            if prov_code not in municipalities:
                if city is None or city["name"] in exclude_names:
                    item["level"] = 2
                    item["parent_code"] = prov_code
                    self.city_exporter.export_item(item)
                else:
                    if item["name"] in exclude_names:
                        pass
                    else:
                        item["level"] = 3
                        item["parent_code"] = city_code
                        self.county_exporter.export_item(item)
            else:
                item["level"] = 3
                item["parent_code"] = city_code
                self.county_exporter.export_item(item)
