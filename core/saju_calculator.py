# 천간, 지지 기반 사주 계산
CHEONGAN = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
JIJI = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

def get_year_ganji(year: int) -> str:
    return CHEONGAN[(year - 4) % 10] + JIJI[(year - 4) % 12]

def get_saju_info(birth_date: str, birth_time: str = None) -> dict:
    """birth_date: 'YYYY-MM-DD' 형식"""
    year, month, day = map(int, birth_date.split("-"))
    year_ganji = get_year_ganji(year)

    return {
        "year": year,
        "month": month,
        "day": day,
        "year_ganji": year_ganji,
        "birth_time": birth_time or "미입력"
    }
