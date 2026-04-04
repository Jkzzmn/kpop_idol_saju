from datetime import date

CHEONGAN = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
JIJI = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

CHEONGAN_OHANG = {
    "갑": "목", "을": "목", "병": "화", "정": "화",
    "무": "토", "기": "토", "경": "금", "신": "금",
    "임": "수", "계": "수"
}
JIJI_OHANG = {
    "자": "수", "축": "토", "인": "목", "묘": "목",
    "진": "토", "사": "화", "오": "화", "미": "토",
    "신": "금", "유": "금", "술": "토", "해": "수"
}

MONTH_JIJI = ["인", "묘", "진", "사", "오", "미", "신", "유", "술", "해", "자", "축"]
MONTH_CHEONGAN = {
    "갑": ["병","정","무","기","경","신","임","계","갑","을","병","정"],
    "을": ["무","기","경","신","임","계","갑","을","병","정","무","기"],
    "병": ["경","신","임","계","갑","을","병","정","무","기","경","신"],
    "정": ["임","계","갑","을","병","정","무","기","경","신","임","계"],
    "무": ["갑","을","병","정","무","기","경","신","임","계","갑","을"],
    "기": ["병","정","무","기","경","신","임","계","갑","을","병","정"],
    "경": ["무","기","경","신","임","계","갑","을","병","정","무","기"],
    "신": ["경","신","임","계","갑","을","병","정","무","기","경","신"],
    "임": ["임","계","갑","을","병","정","무","기","경","신","임","계"],
    "계": ["갑","을","병","정","무","기","경","신","임","계","갑","을"],
}

HOUR_JIJI_LIST = ["자","축","인","묘","진","사","오","미","신","유","술","해"]
HOUR_RANGE = [(23,1),(1,3),(3,5),(5,7),(7,9),(9,11),(11,13),(13,15),(15,17),(17,19),(19,21),(21,23)]

DAY_TO_HOUR_GAN = {
    "갑": ["갑","을","병","정","무","기","경","신","임","계","갑","을"],
    "을": ["병","정","무","기","경","신","임","계","갑","을","병","정"],
    "병": ["무","기","경","신","임","계","갑","을","병","정","무","기"],
    "정": ["경","신","임","계","갑","을","병","정","무","기","경","신"],
    "무": ["임","계","갑","을","병","정","무","기","경","신","임","계"],
    "기": ["갑","을","병","정","무","기","경","신","임","계","갑","을"],
    "경": ["병","정","무","기","경","신","임","계","갑","을","병","정"],
    "신": ["무","기","경","신","임","계","갑","을","병","정","무","기"],
    "임": ["경","신","임","계","갑","을","병","정","무","기","경","신"],
    "계": ["임","계","갑","을","병","정","무","기","경","신","임","계"],
}

BASE_DATE = date(1900, 1, 1)

def get_year_ganji(year: int) -> tuple:
    return CHEONGAN[(year - 4) % 10], JIJI[(year - 4) % 12]

def get_month_ganji(year: int, month: int) -> tuple:
    year_gan, _ = get_year_ganji(year)
    return MONTH_CHEONGAN[year_gan][month - 1], MONTH_JIJI[month - 1]

def get_day_ganji(birth_date: date) -> tuple:
    delta = (birth_date - BASE_DATE).days
    return CHEONGAN[delta % 10], JIJI[delta % 12]

def get_hour_ganji(hour: int, day_gan: str) -> tuple:
    for i, (start, end) in enumerate(HOUR_RANGE):
        if start == 23:
            if hour >= 23 or hour < 1:
                ji = HOUR_JIJI_LIST[i]
                return DAY_TO_HOUR_GAN[day_gan][i], ji
        elif start <= hour < end:
            ji = HOUR_JIJI_LIST[i]
            return DAY_TO_HOUR_GAN[day_gan][i], ji
    return DAY_TO_HOUR_GAN[day_gan][0], HOUR_JIJI_LIST[0]

def calculate_saju(birth_date: date, birth_hour: int = None) -> dict:
    year_gan, year_ji = get_year_ganji(birth_date.year)
    month_gan, month_ji = get_month_ganji(birth_date.year, birth_date.month)
    day_gan, day_ji = get_day_ganji(birth_date)

    pillars = {
        "년주": {"천간": year_gan, "지지": year_ji},
        "월주": {"천간": month_gan, "지지": month_ji},
        "일주": {"천간": day_gan, "지지": day_ji},
    }

    if birth_hour is not None:
        hour_gan, hour_ji = get_hour_ganji(birth_hour, day_gan)
        pillars["시주"] = {"천간": hour_gan, "지지": hour_ji}

    # 오행 카운트
    ohang_count = {"목": 0, "화": 0, "토": 0, "금": 0, "수": 0}
    for p in pillars.values():
        ohang_count[CHEONGAN_OHANG[p["천간"]]] += 1
        ohang_count[JIJI_OHANG[p["지지"]]] += 1

    return {"pillars": pillars, "ohang_count": ohang_count}