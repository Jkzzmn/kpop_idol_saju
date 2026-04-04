from collections import Counter
from datetime import datetime
from typing import Optional, Dict, Any

from sajupy import SajuCalculator

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

KOR_STEM = {
    "甲": "갑", "乙": "을", "丙": "병", "丁": "정", "戊": "무",
    "己": "기", "庚": "경", "辛": "신", "壬": "임", "癸": "계",
}

KOR_BRANCH = {
    "子": "자", "丑": "축", "寅": "인", "卯": "묘", "辰": "진", "巳": "사",
    "午": "오", "未": "미", "申": "신", "酉": "유", "戌": "술", "亥": "해",
}

calculator = SajuCalculator()


def normalize_birth_input(
    birth_date: str,
    birth_time: Optional[str] = None
) -> tuple[int, int, int, int, int, bool]:
    has_birth_time = bool(birth_time and str(birth_time).strip())
    dt_str = f"{birth_date} {birth_time if has_birth_time else '12:00'}"
    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    return dt.year, dt.month, dt.day, dt.hour, dt.minute, has_birth_time


def remove_hour_pillar_if_no_time(saju_result: Dict[str, Any], has_birth_time: bool) -> Dict[str, Any]:
    if has_birth_time:
        return saju_result

    cleaned = dict(saju_result)
    for key in [
        "hour_stem",
        "hour_branch",
        "hour_pillar",
        "hour_stem_hanja",
        "hour_branch_hanja",
    ]:
        if key in cleaned:
            cleaned[key] = None
    return cleaned


def count_five_elements(saju_result: Dict[str, Any]) -> Dict[str, int]:
    counted = Counter({"목": 0, "화": 0, "토": 0, "금": 0, "수": 0})

    stems = [
        saju_result["year_stem"],
        saju_result["month_stem"],
        saju_result["day_stem"],
    ]
    branches = [
        saju_result["year_branch"],
        saju_result["month_branch"],
        saju_result["day_branch"],
    ]

    if saju_result.get("hour_stem"):
        stems.append(saju_result["hour_stem"])
    if saju_result.get("hour_branch"):
        branches.append(saju_result["hour_branch"])

    for s in stems:
        counted[STEM_TO_ELEMENT[s]] += 1

    for b in branches:
        counted[BRANCH_TO_ELEMENT[b]] += 1

    return dict(counted)


def build_pillars(saju_result: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
    pillars = {
        "year": {
            "stem": saju_result["year_stem"],
            "branch": saju_result["year_branch"],
            "stem_kr": KOR_STEM[saju_result["year_stem"]],
            "branch_kr": KOR_BRANCH[saju_result["year_branch"]],
            "stem_element": STEM_TO_ELEMENT[saju_result["year_stem"]],
            "branch_element": BRANCH_TO_ELEMENT[saju_result["year_branch"]],
        },
        "month": {
            "stem": saju_result["month_stem"],
            "branch": saju_result["month_branch"],
            "stem_kr": KOR_STEM[saju_result["month_stem"]],
            "branch_kr": KOR_BRANCH[saju_result["month_branch"]],
            "stem_element": STEM_TO_ELEMENT[saju_result["month_stem"]],
            "branch_element": BRANCH_TO_ELEMENT[saju_result["month_branch"]],
        },
        "day": {
            "stem": saju_result["day_stem"],
            "branch": saju_result["day_branch"],
            "stem_kr": KOR_STEM[saju_result["day_stem"]],
            "branch_kr": KOR_BRANCH[saju_result["day_branch"]],
            "stem_element": STEM_TO_ELEMENT[saju_result["day_stem"]],
            "branch_element": BRANCH_TO_ELEMENT[saju_result["day_branch"]],
        },
    }

    if saju_result.get("hour_stem") and saju_result.get("hour_branch"):
        pillars["hour"] = {
            "stem": saju_result["hour_stem"],
            "branch": saju_result["hour_branch"],
            "stem_kr": KOR_STEM[saju_result["hour_stem"]],
            "branch_kr": KOR_BRANCH[saju_result["hour_branch"]],
            "stem_element": STEM_TO_ELEMENT[saju_result["hour_stem"]],
            "branch_element": BRANCH_TO_ELEMENT[saju_result["hour_branch"]],
        }

    return pillars


def calculate_saju_data(
    birth_date: str,
    birth_time: Optional[str] = None,
    city: str = "Seoul",
    use_solar_time: bool = False,
) -> Dict[str, Any]:
    year, month, day, hour, minute, has_birth_time = normalize_birth_input(birth_date, birth_time)

    result = calculator.calculate_saju(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        city=city,
        use_solar_time=use_solar_time,
        utc_offset=9,
        early_zi_time=True,
    )

    result = remove_hour_pillar_if_no_time(result, has_birth_time)

    pillars = build_pillars(result)
    five_elements = count_five_elements(result)

    return {
        "birth_date": birth_date,
        "birth_time": birth_time if has_birth_time else None,
        "pillars": pillars,
        "day_master": result["day_stem"],
        "day_master_kr": KOR_STEM[result["day_stem"]],
        "five_elements": five_elements,
        "raw": result,
        "has_birth_time": has_birth_time,
    }
