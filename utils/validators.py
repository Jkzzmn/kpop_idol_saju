from datetime import datetime

def validate_inputs(name: str, birth_date: str, gender: str) -> tuple[bool, str]:
    if not name.strip():
        return False, "이름을 입력해주세요."
    try:
        datetime.strptime(birth_date, "%Y-%m-%d")
    except ValueError:
        return False, "날짜 형식이 올바르지 않습니다. (예: 1995-03-15)"
    if gender not in ["남성", "여성"]:
        return False, "성별을 선택해주세요."
    return True, ""
