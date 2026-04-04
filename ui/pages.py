import streamlit as st
from datetime import date, datetime


def init_state():
    defaults = {
        "step": "home",
        "my_info": {},
        "match_type": None,
        "partner_info": {},
        "result": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def validate_time_str(value: str) -> bool:
    if not value:
        return True
    try:
        datetime.strptime(value, "%H:%M")
        return True
    except ValueError:
        return False


def render_home():
    st.markdown("# 🇰🇷 Saju Match")
    st.markdown("당신과 누군가의 오행 궁합을 분석해보세요.")
    st.markdown("친구, 연인, 그리고 K-pop idol까지 비교할 수 있습니다.")

    if st.button("시작하기", use_container_width=True):
        st.session_state.step = "my_info"
        st.rerun()


def render_my_info():
    st.markdown("## 1. 내 정보 입력")

    first_name = st.text_input("First Name", key="my_first_name")
    last_name = st.text_input("Last Name", key="my_last_name")
    gender = st.selectbox("성별", ["남성", "여성"], key="my_gender")
    birth_date = st.date_input(
        "Birth",
        value=date(1998, 1, 1),
        min_value=date(1900, 1, 1),
        max_value=date.today(),
        format="YYYY-MM-DD",
        key="my_birth_date"
    )

    use_time = st.checkbox("Birth Time 입력 (선택)", key="my_use_time")
    birth_time = None
    if use_time:
        raw_time = st.text_input(
            "Birth Time",
            placeholder="예: 14:30",
            key="my_birth_time_input"
        ).strip()
        birth_time = raw_time or None

    if st.button("다음", use_container_width=True, key="my_info_next"):
        if not first_name.strip() and not last_name.strip():
            st.error("이름을 입력해주세요.")
            return
        if birth_time and not validate_time_str(birth_time):
            st.error("Birth Time은 HH:MM 형식으로 입력해주세요. 예: 14:30")
            return

        st.session_state.my_info = {
            "name": f"{first_name} {last_name}".strip(),
            "gender": gender,
            "birth_date": birth_date.strftime("%Y-%m-%d"),
            "birth_time": birth_time,
        }
        st.session_state.step = "match_type"
        st.rerun()


def render_match_type():
    st.markdown("## 2. 궁합 종류 선택")

    choice = st.radio(
        "어떤 궁합을 볼까요?",
        ["친구", "연인", "K-pop Idol"],
        horizontal=False,
        key="match_type_radio"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("이전", use_container_width=True, key="match_type_prev"):
            st.session_state.step = "my_info"
            st.rerun()
    with col2:
        if st.button("다음", use_container_width=True, key="match_type_next"):
            st.session_state.match_type = choice
            st.session_state.step = "partner_info"
            st.rerun()


def render_partner_info():
    match_type = st.session_state.match_type
    st.markdown(f"## 3. 상대 정보 입력 - {match_type}")

    if match_type in ["친구", "연인"]:
        first_name = st.text_input("상대 First Name", key="partner_first_name")
        last_name = st.text_input("상대 Last Name", key="partner_last_name")
        gender = st.selectbox("상대 성별", ["남성", "여성"], key="partner_gender")
        birth_date = st.date_input(
            "상대 Birth",
            value=date(1998, 1, 1),
            min_value=date(1900, 1, 1),
            max_value=date.today(),
            format="YYYY-MM-DD",
            key="partner_birth_date"
        )

        use_time = st.checkbox("상대 Birth Time 입력 (선택)", key="partner_use_time")
        birth_time = None
        if use_time:
            raw_time = st.text_input(
                "상대 Birth Time",
                placeholder="예: 08:20",
                key="partner_birth_time_input"
            ).strip()
            birth_time = raw_time or None

        if st.button("결과 보기", use_container_width=True, key="partner_submit"):
            if not first_name.strip() and not last_name.strip():
                st.error("상대 이름을 입력해주세요.")
                return
            if birth_time and not validate_time_str(birth_time):
                st.error("상대 Birth Time은 HH:MM 형식으로 입력해주세요. 예: 08:20")
                return

            st.session_state.partner_info = {
                "name": f"{first_name} {last_name}".strip(),
                "gender": gender,
                "birth_date": birth_date.strftime("%Y-%m-%d"),
                "birth_time": birth_time,
            }
            st.session_state.step = "result"
            st.rerun()

    else:
        idol_name = st.text_input(
            "아이돌 이름",
            placeholder="예: G-Dragon, IU, Lisa",
            key="idol_name_input"
        )

        if st.button("결과 보기", use_container_width=True, key="idol_submit"):
            if not idol_name.strip():
                st.error("아이돌 이름을 입력해주세요.")
                return

            st.session_state.partner_info = {
                "idol_name": idol_name.strip()
            }
            st.session_state.step = "result"
            st.rerun()
