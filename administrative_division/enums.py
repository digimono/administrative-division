# -*- coding: utf-8 -*-

from enum import Enum, unique

"""
https://baike.baidu.com/item/%E5%A4%A7%E5%8C%BA/22105431
https://baike.baidu.com/item/%E6%B8%AF%E6%BE%B3%E5%8F%B0
"""


@unique
class ChinaRegion(Enum):
    """
    华东地区（上海、江苏、浙江、安徽、福建、江西、山东）
    """
    East = 1

    """
    Southern China/South China
    华南地区（广东、广西、海南）
    """
    South = 2

    """    
    华中地区（河南、湖北、湖南）
    """
    Central = 3

    """    
    华北地区（北京、天津、河北、山西、内蒙古）
    """
    North = 4

    """
    西北地区（宁夏、新疆、青海、陕西、甘肃）
    """
    Northwest = 5

    """
    西南地区（四川、云南、贵州、西藏、重庆）
    """
    Southwest = 6

    """
    东北地区（辽宁、吉林、黑龙江）
    """
    Northeast = 7

    """
    台港澳地区（香港、澳门、台湾）
    """
    HK_MAC_TW = 8
