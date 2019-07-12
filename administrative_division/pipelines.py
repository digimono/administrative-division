# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import logging

from scrapy.exceptions import DropItem

# from collections import Counter

logger = logging.getLogger(__name__)

exclude_names = ["市辖区", "县", "省直辖县级行政区划", "自治区直辖县级行政区划"]
# 直辖市
municipalities = [110000, 120000, 310000, 500000]
# 自治区
autonomous_regions = [150000, 450000, 540000, 640000, 650000]
# 特别行政区
special_administrative_regions = [810000, 820000]


# 华东（East China）
# 东北（Northeast China）
# 华北（North China）
# 中南（South Central China）
# 华中（Central China）
# 华南（Southern China/South China）
# 西部（Western China）
# 西北（Northwest China）
# 西南（Southwest China）

class AdministrativeDivisionPipeline(object):
    def process_item(self, item, spider):
        sep = "\u3000"

        area = item["area"]
        # item["area"] = None

        # counter = Counter(area)
        # item["level"] = counter[sep]
        item["level"] = area.count(sep)

        if area.startswith("000000"):
            item["code"] = 0
            item["name"] = "中国"
        else:
            arr = area.split(sep)
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

        del item["area"]
        return item


class AssemPipeline(object):
    def __init__(self):
        self.rawDict = {}
        self.provDict = {}
        self.cityDict = {}
        self.countyDict = {}

    def process_item(self, item, spider):
        code = item["code"]
        self.rawDict[code] = dict(item)
        self.assem_province(code, item)

        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.assem_city()
        self.assem_county()

        logger.info(json.dumps(self.provDict, ensure_ascii=False))
        logger.info(json.dumps(self.cityDict, ensure_ascii=False))
        logger.info(json.dumps(self.countyDict, ensure_ascii=False))

    def assem_province(self, code, item):
        if self.is_prov(code):
            province = dict(item)
            province["parent_code"] = 0
            province["children"] = []

            self.provDict[code] = province

    def assem_city(self):
        for code in list(self.rawDict.keys()):
            if not self.is_city(code):
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
            if not self.is_county(code):
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

    def is_prov(self, code):
        code_str = str(code)
        return len(code_str) == 6 and code_str.endswith("0000")

    def is_city(self, code):
        code_str = str(code)
        return (not self.is_prov(code)) and code_str.endswith("00")

    def is_county(self, code):
        code_str = str(code)
        return len(code_str) == 6 and (not self.is_prov(code)) and (not self.is_city(code))

    def check_duplicate(self, items, it, key):
        if len(items) == 0:
            return False

        for item in items:
            if item[key] == it[key]:
                return True

        return False
