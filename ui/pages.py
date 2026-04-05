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


def _step_indicator(current: int):
    steps = ["내 정보", "궁합 선택", "상대 정보", "결과"]

    dot_parts = []
    for i in range(1, len(steps) + 1):
        if i < current:
            c, s = "#a78bfa", "8px"
        elif i == current:
            c, s = "#ffffff", "10px"
        else:
            c, s = "rgba(255,255,255,0.2)", "8px"
        dot_parts.append(
            "<div style='width:{s};height:{s};border-radius:50%;background:{c};margin:0 4px;'></div>".format(s=s, c=c)
        )

    label_parts = []
    for i, l in enumerate(steps, 1):
        if i < current:
            color, weight = "#a78bfa", "400"
        elif i == current:
            color, weight = "white", "700"
        else:
            color, weight = "rgba(255,255,255,0.25)", "400"
        label_parts.append(
            "<span style='font-size:10px;color:{c};margin:0 8px;font-weight:{w};'>{l}</span>".format(
                c=color, w=weight, l=l
            )
        )

    st.markdown(
        "<div style='display:flex;flex-direction:column;align-items:center;padding:16px 0 8px 0;'>"
        "<div style='display:flex;align-items:center;margin-bottom:8px;'>{dots}</div>"
        "<div style='display:flex;'>{labels}</div>"
        "</div>".format(dots="".join(dot_parts), labels="".join(label_parts)),
        unsafe_allow_html=True,
    )


# ────────────────────────────────────────
# STEP 1 — 홈
# ────────────────────────────────────────
def render_home():
    st.markdown("""
    <div style="min-height:75vh;display:flex;flex-direction:column;
                align-items:center;justify-content:center;text-align:center;padding:40px 20px;">
        <div style="font-size:64px;margin-bottom:16px;">🌙</div>
        <div style="font-size:12px;font-weight:700;color:#a78bfa;letter-spacing:0.15em;
                    text-transform:uppercase;margin-bottom:10px;">Korean Saju</div>
        <div style="font-size:36px;font-weight:900;color:white;line-height:1.2;margin-bottom:10px;">
            사주 궁합
        </div>
        <div style="font-size:15px;color:rgba(255,255,255,0.5);margin-bottom:44px;line-height:1.75;">
            당신과 친구, 연인,<br>그리고 K-pop 아이돌까지<br>오행으로 보는 관계 분석
        </div>
        <div style="display:flex;gap:32px;margin-bottom:8px;">
            <div style="text-align:center;">
                <div style="font-size:30px;">🤝</div>
                <div style="font-size:11px;color:rgba(255,255,255,0.4);margin-top:6px;">친구</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:30px;">💕</div>
                <div style="font-size:11px;color:rgba(255,255,255,0.4);margin-top:6px;">연인</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:30px;">⭐</div>
                <div style="font-size:11px;color:rgba(255,255,255,0.4);margin-top:6px;">아이돌</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("✨  궁합 보러 가기", use_container_width=True):
        st.session_state.step = "my_info"
        st.rerun()

    st.markdown(
        "<div style='text-align:center;margin-top:14px;'>"
        "<span style='font-size:12px;color:rgba(255,255,255,0.2);'>Touch anywhere to start</span>"
        "</div>",
        unsafe_allow_html=True,
    )


# ────────────────────────────────────────
# STEP 2 — 내 정보 입력
# ────────────────────────────────────────
def render_my_info():
    _step_indicator(1)

    st.markdown(
        "<div style='padding:16px 0 20px 0;'>"
        "<div style='font-size:22px;font-weight:800;color:white;'>내 정보 입력</div>"
        "<div style='font-size:13px;color:#a78bfa;margin-top:6px;'>사주 계산을 위해 생년월일을 입력해주세요</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name", key="my_first_name", placeholder="길동")
    with col2:
        last_name = st.text_input("Last Name", key="my_last_name", placeholder="홍")

    gender = st.selectbox("성별", ["남성", "여성"], key="my_gender")

    birth_date = st.date_input(
        "Birth",
        value=date(1998, 1, 1),
        min_value=date(1900, 1, 1),
        max_value=date.today(),
        format="YYYY-MM-DD",
        key="my_birth_date",
    )

    use_time = st.checkbox("I Know Birth Time!", key="my_use_time")
    birth_time = None
    if use_time:
        raw_time = st.text_input(
            "Birth Time",
            placeholder="예: 14:30",
            key="my_birth_time_input",
        ).strip()
        birth_time = raw_time or None

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    if st.button("다음  →", use_container_width=True, key="my_info_next"):
        if not first_name.strip() and not last_name.strip():
            st.error("이름을 입력해주세요.")
            return
        if birth_time and not validate_time_str(birth_time):
            st.error("Birth Time은 HH:MM 형식으로 입력해주세요. 예: 14:30")
            return

        st.session_state.my_info = {
            "name": (first_name + " " + last_name).strip(),
            "gender": gender,
            "birth_date": birth_date.strftime("%Y-%m-%d"),
            "birth_time": birth_time,
        }
        st.session_state.step = "match_type"
        st.rerun()


# ────────────────────────────────────────
# STEP 3 — 궁합 종류 선택
# ────────────────────────────────────────
def render_match_type():
    _step_indicator(2)

    st.markdown(
        "<div style='padding:16px 0 20px 0;'>"
        "<div style='font-size:22px;font-weight:800;color:white;'>궁합 종류 선택</div>"
        "<div style='font-size:13px;color:#a78bfa;margin-top:6px;'>어떤 관계의 궁합을 볼까요?</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    # 카드형 선택 버튼 (st.radio 대신 직접 버튼 3개)
    if "match_type_selected" not in st.session_state:
        st.session_state.match_type_selected = "친구"

    options = [
        ("친구", "🤝", "친구와의 오행 궁합을 분석합니다"),
        ("연인", "💕", "연인과의 오행 궁합을 분석합니다"),
        ("K-pop Idol", "⭐", "K-pop 아이돌과의 오행 궁합을 분석합니다"),
    ]

    for value, emoji, desc in options:
        selected = st.session_state.match_type_selected == value
        border_color = "#a78bfa" if selected else "rgba(167,139,250,0.2)"
        bg_color = "rgba(124,58,237,0.25)" if selected else "rgba(255,255,255,0.06)"
        text_color = "white" if selected else "#ddd6fe"
        check = "✓  " if selected else ""

        st.markdown(
            "<div style='background:{bg};border:1.5px solid {border};"
            "border-radius:14px;padding:14px 18px;margin-bottom:10px;cursor:pointer;'>"
            "<div style='display:flex;align-items:center;gap:12px;'>"
            "<span style='font-size:26px;'>{emoji}</span>"
            "<div>"
            "<div style='font-size:15px;font-weight:700;color:{text};'>{check}{value}</div>"
            "<div style='font-size:12px;color:rgba(196,181,253,0.7);margin-top:2px;'>{desc}</div>"
            "</div></div></div>".format(
                bg=bg_color, border=border_color, emoji=emoji,
                text=text_color, check=check, value=value, desc=desc
            ),
            unsafe_allow_html=True,
        )
        if st.button(value, key="card_" + value, use_container_width=True):
            st.session_state.match_type_selected = value
            st.rerun()

    # 버튼을 카드 위에 투명하게 겹치는 방식은 Streamlit 제약으로 불가,
    # 대신 버튼을 카드 바로 아래에 배치하되 시각적으로 숨김 처리
    st.markdown("""
    <style>
    button[kind="secondary"][data-testid*="card_"] {
        opacity: 0 !important;
        height: 1px !important;
        margin-top: -10px !important;
        margin-bottom: 0 !important;
        padding: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("←  이전", use_container_width=True, key="match_type_prev"):
            st.session_state.step = "my_info"
            st.rerun()
    with col2:
        if st.button("다음  →", use_container_width=True, key="match_type_next"):
            st.session_state.match_type = st.session_state.match_type_selected
            st.session_state.step = "partner_info"
            st.rerun()


# ────────────────────────────────────────
# STEP 4 — 상대 정보 입력
# ────────────────────────────────────────
def render_partner_info():
    _step_indicator(3)
    match_type = st.session_state.match_type

    type_label_map = {"친구": "🤝 친구", "연인": "💕 연인", "K-pop Idol": "⭐ K-pop Idol"}
    type_label = type_label_map.get(match_type, match_type)

    st.markdown(
        "<div style='padding:16px 0 20px 0;'>"
        "<div style='font-size:22px;font-weight:800;color:white;'>{label} 정보 입력</div>"
        "<div style='font-size:13px;color:#a78bfa;margin-top:6px;'>상대방 정보를 입력해주세요</div>"
        "</div>".format(label=type_label),
        unsafe_allow_html=True,
    )

    if match_type in ["친구", "연인"]:
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("상대 First Name", key="partner_first_name", placeholder="민지")
        with col2:
            last_name = st.text_input("상대 Last Name", key="partner_last_name", placeholder="김")

        gender = st.selectbox("상대 성별", ["남성", "여성"], key="partner_gender")
        birth_date = st.date_input(
            "상대 Birth",
            value=date(1998, 1, 1),
            min_value=date(1900, 1, 1),
            max_value=date.today(),
            format="YYYY-MM-DD",
            key="partner_birth_date",
        )

        use_time = st.checkbox("I Know Birth Time!", key="partner_use_time")
        birth_time = None
        if use_time:
            raw_time = st.text_input(
                "상대 Birth Time",
                placeholder="예: 08:20",
                key="partner_birth_time_input",
            ).strip()
            birth_time = raw_time or None

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("←  이전", use_container_width=True, key="partner_prev"):
                st.session_state.step = "match_type"
                st.rerun()
        with col2:
            if st.button("결과 보기  ✨", use_container_width=True, key="partner_submit"):
                if not first_name.strip() and not last_name.strip():
                    st.error("상대 이름을 입력해주세요.")
                    return
                if birth_time and not validate_time_str(birth_time):
                    st.error("Birth Time은 HH:MM 형식으로 입력해주세요.")
                    return
                st.session_state.partner_info = {
                    "name": (first_name + " " + last_name).strip(),
                    "gender": gender,
                    "birth_date": birth_date.strftime("%Y-%m-%d"),
                    "birth_time": birth_time,
                }
                st.session_state.step = "result"
                st.rerun()

    else:
        st.markdown(
            "<div style='background:rgba(167,139,250,0.1);border:1px solid rgba(167,139,250,0.25);"
            "border-radius:14px;padding:14px 18px;margin-bottom:20px;'>"
            "<div style='font-size:13px;color:rgba(255,255,255,0.75);line-height:1.7;'>"
            "💡 아이돌 이름을 입력하면 "
            "생년월일을 자동으로 찾아 궁합을 계산합니다"
            "</div></div>",
            unsafe_allow_html=True,
        )

        idol_name = st.text_input(
            "아이돌 이름",
            placeholder="예: G-Dragon, IU, Lisa, Jungkook",
            key="idol_name_input",
        )

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("←  이전", use_container_width=True, key="idol_prev"):
                st.session_state.step = "match_type"
                st.rerun()
        with col2:
            if st.button("결과 보기  ✨", use_container_width=True, key="idol_submit"):
                if not idol_name.strip():
                    st.error("아이돌 이름을 입력해주세요.")
                    return
                st.session_state.partner_info = {"idol_name": idol_name.strip()}
                st.session_state.step = "result"
                st.rerun()