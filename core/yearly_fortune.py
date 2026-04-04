from datetime import date
from typing import Dict

HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

KOR_STEM = {
    "甲": "갑", "乙": "을", "丙": "병", "丁": "정", "戊": "무",
    "己": "기", "庚": "경", "辛": "신", "壬": "임", "癸": "계",
}

KOR_BRANCH = {
    "子": "자", "丑": "축", "寅": "인", "卯": "묘", "辰": "진", "巳": "사",
    "午": "오", "未": "미", "申": "신", "酉": "유", "戌": "술", "亥": "해",
}

STEM_TO_ELEMENT = {
    "甲": "목", "乙": "목",
    "丙": "화", "丁": "화",
    "戊": "토", "己": "토",
    "庚": "금", "辛": "금",
    "壬": "수", "癸": "수",
}

BRANCH_TO_ELEMENT = {
    "子": "수", "丑": "토",
    "寅": "목", "卯": "목",
    "辰": "토", "巳": "화",
    "午": "화", "未": "토",
    "申": "금", "酉": "금",
    "戌": "토", "亥": "수",
}


def get_year_ganzhi(year: int) -> Dict[str, str]:
    stem = HEAVENLY_STEMS[(year - 4) % 10]
    branch = EARTHLY_BRANCHES[(year - 4) % 12]

    return {
        "year": year,
        "stem": stem,
        "branch": branch,
        "pillar": f"{stem}{branch}",
        "stem_kr": KOR_STEM[stem],
        "branch_kr": KOR_BRANCH[branch],
        "stem_element": STEM_TO_ELEMENT[stem],
        "branch_element": BRANCH_TO_ELEMENT[branch],
    }


def get_current_year_fortune() -> Dict[str, str]:
    return get_year_ganzhi(date.today().year)
