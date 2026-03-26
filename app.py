import streamlit as st
from datetime import date
from core.prompt_builder import build_saju_prompt
from core.saju_calculator import get_saju_info
from core.gemini_client import generate
from utils.validators import validate_inputs


st.set_page_config(page_title="AI 사주 풀이", page_icon="🔮")
st.title("Elements AI 사주 풀이")
st.caption("AI가 사주를 분석해드립니다.")

with st.form("saju_form"):
    name = st.text_input("이름", placeholder="홍길동")
    birth_date = st.date_input(
        "생년월일",
        value=date(1995, 1, 1),          # 기본값
        min_value=date(1900, 1, 1),      # 최소 1900년
        max_value=date.today(),           # 최대 오늘
        format="YYYY-MM-DD"
    )
    gender = st.radio("성별", ["남성", "여성"], horizontal=True)
    birth_time = st.selectbox(
        "태어난 시간 (선택)",
        ["미입력", "자시(23~01)", "축시(01~03)", "인시(03~05)", "묘시(05~07)",
         "진시(07~09)", "사시(09~11)", "오시(11~13)", "미시(13~15)",
         "신시(15~17)", "유시(17~19)", "술시(19~21)", "해시(21~23)"]
    )
    submitted = st.form_submit_button("사주 풀이")

if submitted:
    birth_date_str = birth_date.strftime("%Y-%m-%d")
    time_input = None if birth_time == "미입력" else birth_time

    is_valid, error_msg = validate_inputs(name, birth_date_str, gender)
    if not is_valid:
        st.error(error_msg)
    else:
        saju_info = get_saju_info(birth_date_str, time_input)
        prompt = build_saju_prompt(name, birth_date_str, gender, time_input)

        with st.spinner("사주를 분석 중입니다..."):
            result = generate(prompt)

        st.success("분석 완료!")
        st.markdown("---")
        st.markdown(result)
