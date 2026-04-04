from typing import Dict

STEM_ELEMENT = {
    "甲": "목", "乙": "목",
    "丙": "화", "丁": "화",
    "戊": "토", "己": "토",
    "庚": "금", "辛": "금",
    "壬": "수", "癸": "수",
}

STEM_YINYANG = {
    "甲": "양", "乙": "음",
    "丙": "양", "丁": "음",
    "戊": "양", "己": "음",
    "庚": "양", "辛": "음",
    "壬": "양", "癸": "음",
}

GENERATES = {
    "목": "화",
    "화": "토",
    "토": "금",
    "금": "수",
    "수": "목",
}

CONTROLS = {
    "목": "토",
    "토": "수",
    "수": "화",
    "화": "금",
    "금": "목",
}


def get_relation(day_master: str, target_stem: str) -> str:
    dm_elem = STEM_ELEMENT[day_master]
    tg_elem = STEM_ELEMENT[target_stem]

    if dm_elem == tg_elem:
        return "same"
    if GENERATES[dm_elem] == tg_elem:
        return "output"
    if GENERATES[tg_elem] == dm_elem:
        return "resource"
    if CONTROLS[dm_elem] == tg_elem:
        return "wealth"
    if CONTROLS[tg_elem] == dm_elem:
        return "power"
    raise ValueError(f"Unexpected relation: {day_master}, {target_stem}")


def get_ten_god(day_master: str, target_stem: str) -> str:
    if day_master == target_stem:
        return "일원"

    relation = get_relation(day_master, target_stem)
    same_polarity = STEM_YINYANG[day_master] == STEM_YINYANG[target_stem]

    mapping = {
        ("same", True): "비견",
        ("same", False): "겁재",
        ("output", True): "식신",
        ("output", False): "상관",
        ("resource", True): "편인",
        ("resource", False): "정인",
        ("wealth", True): "편재",
        ("wealth", False): "정재",
        ("power", True): "편관",
        ("power", False): "정관",
    }
    return mapping[(relation, same_polarity)]


def calculate_ten_gods(pillars: Dict[str, Dict[str, str]], day_master: str) -> Dict[str, str]:
    result = {}
    for pillar_name, pillar in pillars.items():
        stem = pillar["stem"]
        result[f"{pillar_name}_stem_ten_god"] = get_ten_god(day_master, stem)
    return result
