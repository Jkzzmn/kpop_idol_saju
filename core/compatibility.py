from typing import Dict, Any

ELEMENTS = ["목", "화", "토", "금", "수"]

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


def find_lacking_elements(five_elements: Dict[str, int]) -> list[str]:
    min_value = min(five_elements.get(e, 0) for e in ELEMENTS)
    return [e for e in ELEMENTS if five_elements.get(e, 0) == min_value]


def calc_balance_score(my_elements: Dict[str, int], partner_elements: Dict[str, int]) -> int:
    score = 0
    for e in ELEMENTS:
        diff = abs(my_elements.get(e, 0) - partner_elements.get(e, 0))
        score += max(0, 20 - diff * 5)
    return min(100, score)


def calc_support_score(my_elements: Dict[str, int], partner_elements: Dict[str, int]) -> int:
    score = 0
    for my_lack in find_lacking_elements(my_elements):
        supporter = None
        for src, dst in GENERATES.items():
            if dst == my_lack:
                supporter = src
                break
        if supporter:
            score += min(20, partner_elements.get(supporter, 0) * 5)
    return min(100, score)


def calc_conflict_score(my_elements: Dict[str, int], partner_elements: Dict[str, int]) -> int:
    penalty = 0
    for e in ELEMENTS:
        target = CONTROLS[e]
        if my_elements.get(e, 0) >= 2 and partner_elements.get(target, 0) >= 2:
            penalty += 8
    return min(40, penalty)


def calculate_match(my_elements: Dict[str, int], partner_elements: Dict[str, int]) -> Dict[str, Any]:
    balance = calc_balance_score(my_elements, partner_elements)
    support = calc_support_score(my_elements, partner_elements)
    conflict = calc_conflict_score(my_elements, partner_elements)

    final_score = round(balance * 0.5 + support * 0.35 - conflict * 0.15)
    final_score = max(0, min(100, final_score))

    return {
        "score": final_score,
        "balance_score": balance,
        "support_score": support,
        "conflict_penalty": conflict,
        "my_lacking_elements": find_lacking_elements(my_elements),
        "partner_lacking_elements": find_lacking_elements(partner_elements),
    }
