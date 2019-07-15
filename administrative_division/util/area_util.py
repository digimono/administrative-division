# -*- coding: utf-8 -*-


class Area:
    @staticmethod
    def is_prov(code) -> bool:
        code_str = str(code)
        return len(code_str) == 6 and code_str.endswith("0000")

    @staticmethod
    def is_city(code) -> bool:
        code_str = str(code)
        return len(code_str) == 6 and (not Area.is_prov(code)) and code_str.endswith("00")

    @staticmethod
    def is_county(code) -> bool:
        code_str = str(code)
        return len(code_str) == 6 and (not Area.is_prov(code)) and (not Area.is_city(code))
