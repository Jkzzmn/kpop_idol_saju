import json
from typing import Dict, Any


def build_match_prompt(
    match_type: str,
    my_profile: Dict[str, Any],
    partner_profile: Dict[str, Any],
    match_result: Dict[str, Any],
) -> str:
    if match_type == "친구":
        focus = "서로 편하게 오래 갈 수 있는 관계 유지법, 갈등을 줄이는 소통 방식, 서로의 부족한 오행을 어떻게 보완해줄 수 있는지"
    elif match_type == "연인":
        focus = "더 잘 만나기 위한 방법, 감정 표현 방식, 연애에서 부딪히기 쉬운 지점과 관계를 안정적으로 유지하는 법"
    else:
        focus = "이 아이돌에게 끌리는 이유, 팬으로서 정서적으로 잘 맞는 포인트, 내가 어떤 오행을 보완하면 더 즐겁고 건강하게 덕질할 수 있는지"

    payload = {
        "match_type": match_type,
        "me": my_profile,
        "partner": partner_profile,
        "match_result": match_result,
    }

    return f"""
너는 사주와 관계 해석에 능한 전문 해설가다.

아래 데이터는 이미 코드로 계산 완료된 값이다.
절대 다시 계산하지 말고, 제공된 값만 사용해서 해석하라.
천간, 지지, 오행, 십신 값을 바꾸거나 추정하지 마라.

[계산 데이터]
{json.dumps(payload, ensure_ascii=False, indent=2)}

[해석 초점]
{focus}

[응답 규칙]
- 반드시 JSON으로만 응답
- 코드블록 사용 금지
- 친구/연인/아이돌 관계 유형에 맞는 말만 할 것
- 과장하지 말고 구체적으로 설명할 것
- 상대를 비난하는 표현 금지
- 실천 가능한 조언 포함

[반환 형식]
{{
  "summary": "관계 전체 요약 2~4문장",
  "chemistry": "왜 잘 맞거나 부딪히는지 설명 3~5문장",
  "my_lacking_elements_comment": "나에게 부족한 오행과 보완 방향 설명 2~4문장",
  "partner_lacking_elements_comment": "상대에게 부족한 오행 설명 2~4문장. 단, 아이돌이면 팬 관점으로 짧게 작성",
  "relationship_tip": "관계를 더 좋게 만드는 실천 팁 3~5문장"
}}
""".strip()
