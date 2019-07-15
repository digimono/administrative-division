# -*- coding: utf-8 -*-

from administrative_division.enums import ChinaRegion

EXCLUDE_NAMES = [
    '市辖区',
    '县',
    '省直辖县级行政区划',
    '自治区直辖县级行政区划',
]

# 直辖市
MUNICIPALITIES = [
    110000,
    120000,
    310000,
    500000,
]

# 自治区
AUTONOMOUS_REGIONS = [
    150000,
    450000,
    540000,
    640000,
    650000,
]

# 特别行政区
SPECIAL_ADMINISTRATIVE_REGIONS = [
    810000,
    820000,
]

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
    710000: ChinaRegion.HK_MAC_TW, 810000: ChinaRegion.HK_MAC_TW, 820000: ChinaRegion.HK_MAC_TW,
}
