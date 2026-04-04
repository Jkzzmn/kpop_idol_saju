import streamlit as st

from core.calculator import calculate_saju_data
from core.ten_gods import calculate_ten_gods
from core.yearly_fortune import get_current_year_fortune
from core.prompt_builder import build_match_prompt
from core.gemini_client import generate_interpretation
from core.compatibility import calculate_match
from core.idol_lookup import find_idol
from ui.pages import (
    init_state,
    render_home,
    render_my_info,
    render_match_type,
    render_partner_info,
)

st.set_page_config(page_title="Saju Match", page_icon="🇰🇷", layout="centered")

ELEMENT_COLORS = {
    "목": {"bg": "#E8F5E9", "text": "#2E8B57", "bar": "#2E8B57"},
    "화": {"bg": "#FDECEC", "text": "#D64545", "bar": "#D64545"},
    "토": {"bg": "#FFF8E1", "text": "#C9A227", "bar": "#C9A227"},
    "금": {"bg": "#F1F3F5", "text": "#7A8694", "bar": "#7A8694"},
    "수": {"bg": "#EAF2FF", "text": "#2F5D9F", "bar": "#2F5D9F"},
}

ELEMENT_GOODS = {
    "목": "초록 계열 굿즈, 식물 테마 포토카드, 우드 소재 키링, 녹색 응원봉 슬리브",
    "화": "레드·핑크 계열 굿즈, 불꽃 테마 아크릴 스탠드, 포인트 컬러 포스터, 라이브 공연 굿즈",
    "토": "노란색·베이지 계열 굿즈, 어스 톤 포토북, 도자기 느낌 소품, 빈티지 스타일 엽서",
    "금": "화이트·실버 계열 굿즈, 메탈 배지, 홀로그램 스티커, 미러볼 소품",
    "수": "블루·블랙 계열 굿즈, 야간 콘서트 테마 포토카드, 우주 테마 아크릴, 다크 컬러 후드",
}

ELEMENT_EFFECTS = {
    "목": "성장 에너지·창의력·유연함이 강해져 관계에 생동감이 생깁니다",
    "화": "열정·감정 표현·소통이 활발해져 관계에 온기가 더해집니다",
    "토": "안정감·신뢰·현실감이 높아져 관계의 뿌리가 단단해집니다",
    "금": "결단력·명확한 표현·집중력이 높아져 관계가 정돈됩니다",
    "수": "감수성·직관·깊이가 생겨 관계에 내면적인 유대가 깊어집니다",
}


def render_pillar_table(name: str, pillars: dict, accent_color: str = "#4A90D9"):
    labels = {"year": "연주", "month": "월주", "day": "일주", "hour": "시주"}

    visible_keys = []
    for key in ["year", "month", "day"]:
        if key in pillars:
            visible_keys.append(key)

    if (
        "hour" in pillars
        and pillars["hour"]
        and pillars["hour"].get("stem")
        and pillars["hour"].get("branch")
    ):
        visible_keys.append("hour")

    cards_html = ""
    for key in visible_keys:
        p = pillars[key]
        stem_color = ELEMENT_COLORS[p["stem_element"]]
        branch_color = ELEMENT_COLORS[p["branch_element"]]

        cards_html += f"""
        <div style="flex:1;min-width:0;border:1px solid #e5e7eb;border-radius:18px;padding:12px;background:white;box-shadow:0 1px 4px rgba(0,0,0,0.06);">
            <div style="font-size:12px;color:#888;text-align:center;margin-bottom:8px;">{labels[key]}</div>
            <div style="background:{stem_color['bg']};border-radius:10px;padding:10px;margin-bottom:8px;text-align:center;">
                <div style="font-size:28px;font-weight:800;color:{stem_color['text']};">{p['stem']}</div>
                <div style="font-size:12px;color:{stem_color['text']};">{p['stem_kr']} · {p['stem_element']}</div>
            </div>
            <div style="background:{branch_color['bg']};border-radius:10px;padding:10px;text-align:center;">
                <div style="font-size:28px;font-weight:800;color:{branch_color['text']};">{p['branch']}</div>
                <div style="font-size:12px;color:{branch_color['text']};">{p['branch_kr']} · {p['branch_element']}</div>
            </div>
        </div>
        """

    st.markdown(
        f"""
        <div style="margin-bottom:4px;">
            <span style="font-size:13px;font-weight:600;color:{accent_color};border-left:4px solid {accent_color};padding-left:8px;">
                {name}의 원국
            </span>
        </div>
        <div style="display:flex;gap:8px;margin-bottom:16px;">
            {cards_html}
        </div>
        """,
        unsafe_allow_html=True
    )




def render_five_elements_bar(name: str, five_elements: dict, accent_color: str = "#4A90D9"):
    total = max(sum(five_elements.values()), 1)
    bars_html = ""
    for e in ["목", "화", "토", "금", "수"]:
        val = five_elements.get(e, 0)
        pct = int(val / total * 100)
        color = ELEMENT_COLORS[e]
        bars_html += f"""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
            <div style="width:36px;height:36px;border-radius:10px;background:{color['bg']};display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                <span style="font-size:16px;font-weight:700;color:{color['text']};">{e}</span>
            </div>
            <div style="flex:1;background:#f3f4f6;border-radius:999px;height:18px;overflow:hidden;">
                <div style="width:{pct}%;background:{color['bar']};height:100%;border-radius:999px;transition:width 0.6s ease;"></div>
            </div>
            <div style="width:28px;text-align:right;font-size:14px;font-weight:600;color:#333;">{val}</div>
        </div>
        """

    st.markdown(
        f"""
        <div style="margin-bottom:4px;">
            <span style="font-size:13px;font-weight:600;color:{accent_color};border-left:4px solid {accent_color};padding-left:8px;">
                {name}의 오행
            </span>
        </div>
        <div style="background:white;border:1px solid #e5e7eb;border-radius:16px;padding:16px;margin-bottom:16px;">
            {bars_html}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_element_recommendation(name: str, lacking: list, match_type: str, is_idol_partner: bool = False):
    if not lacking:
        st.markdown(
            f"""
            <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:14px;padding:14px;margin-bottom:16px;">
                <div style="font-size:14px;color:#166534;">✅ {name}은 오행이 고르게 균형 잡혀 있습니다.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    badges_html = ""
    effects_html = ""
    for e in lacking:
        color = ELEMENT_COLORS[e]
        badges_html += f"""
        <span style="display:inline-block;background:{color['bg']};color:{color['text']};border:1px solid {color['text']};border-radius:999px;padding:4px 14px;font-size:14px;font-weight:700;margin-right:6px;margin-bottom:6px;">{e}</span>
        """
        effects_html += f"""
        <div style="display:flex;align-items:flex-start;gap:10px;margin-top:8px;">
            <div style="width:10px;height:10px;border-radius:50%;background:{color['text']};margin-top:5px;flex-shrink:0;"></div>
            <div style="font-size:14px;color:#444;"><b style="color:{color['text']};">{e} 기운</b>을 보완하면: {ELEMENT_EFFECTS[e]}</div>
        </div>
        """

    if is_idol_partner:
        goods_list = "".join([f"<li style='margin-bottom:6px;font-size:14px;color:#555;'>{ELEMENT_GOODS[e]}</li>" for e in lacking])
        goods_section = f"""
        <div style="margin-top:14px;padding-top:12px;border-top:1px solid #e5e7eb;">
            <div style="font-size:13px;font-weight:600;color:#7A8694;margin-bottom:8px;">🛍️ 추천 굿즈 (부족한 오행 기준)</div>
            <ul style="padding-left:18px;margin:0;">{goods_list}</ul>
        </div>
        """
    else:
        goods_section = ""

    label = "나에게" if name == "나" else f"{name}에게"

    st.markdown(
        f"""
        <div style="background:#fafafa;border:1px solid #e5e7eb;border-radius:16px;padding:18px;margin-bottom:16px;">
            <div style="font-size:14px;font-weight:700;color:#222;margin-bottom:10px;">
                💡 {label} 부족한 오행
            </div>
            <div style="margin-bottom:8px;">{badges_html}</div>
            {effects_html}
            {goods_section}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_result():
    my_info = st.session_state.my_info
    partner_info = st.session_state.partner_info
    match_type = st.session_state.match_type

    with st.spinner("내 사주를 계산 중입니다..."):
        my_saju = calculate_saju_data(
            birth_date=my_info["birth_date"],
            birth_time=my_info["birth_time"],
        )
        my_ten_gods = calculate_ten_gods(my_saju["pillars"], my_saju["day_master"])

    if match_type in ["친구", "연인"]:
        with st.spinner("상대 사주를 계산 중입니다..."):
            partner_saju = calculate_saju_data(
                birth_date=partner_info["birth_date"],
                birth_time=partner_info["birth_time"],
            )
            partner_ten_gods = calculate_ten_gods(partner_saju["pillars"], partner_saju["day_master"])
            partner_name = partner_info["name"]
            partner_gender = partner_info["gender"]
    else:
        idol = find_idol(partner_info["idol_name"])
        if not idol:
            st.error("아이돌 정보를 찾지 못했습니다. data/idols.csv를 확인해주세요.")
            if st.button("이전으로"):
                st.session_state.step = "partner_info"
                st.rerun()
            return

        with st.spinner("아이돌 사주를 계산 중입니다..."):
            partner_saju = calculate_saju_data(
                birth_date=idol["birth_date"],
                birth_time=idol["birth_time"],
            )
            partner_ten_gods = calculate_ten_gods(partner_saju["pillars"], partner_saju["day_master"])
            partner_name = idol["name"]
            partner_gender = idol["gender"]

    match_result = calculate_match(
        my_saju["five_elements"],
        partner_saju["five_elements"],
    )

    year_fortune = get_current_year_fortune()

    my_profile = {
        "name": my_info["name"],
        "gender": my_info["gender"],
        "birth_date": my_saju["birth_date"],
        "birth_time": my_saju["birth_time"],
        "pillars": my_saju["pillars"],
        "day_master": my_saju["day_master"],
        "day_master_kr": my_saju["day_master_kr"],
        "five_elements": my_saju["five_elements"],
        "ten_gods": my_ten_gods,
        "year_fortune": year_fortune,
    }

    partner_profile = {
        "name": partner_name,
        "gender": partner_gender,
        "birth_date": partner_saju["birth_date"],
        "birth_time": partner_saju["birth_time"],
        "pillars": partner_saju["pillars"],
        "day_master": partner_saju["day_master"],
        "day_master_kr": partner_saju["day_master_kr"],
        "five_elements": partner_saju["five_elements"],
        "ten_gods": partner_ten_gods,
        "year_fortune": year_fortune,
    }

    with st.spinner("AI가 관계 해석을 작성 중입니다..."):
        prompt = build_match_prompt(
            match_type=match_type,
            my_profile=my_profile,
            partner_profile=partner_profile,
            match_result=match_result,
        )
        ai_result = generate_interpretation(prompt)

    # ─── 헤더 ────────────────────────────────────────
    st.markdown(
        f"""
        <div style="text-align:center;padding:24px 0 8px 0;">
            <div style="font-size:28px;font-weight:800;color:#1a1a1a;">🇰🇷{match_type} 궁합 결과</div>
            <div style="font-size:16px;color:#666;margin-top:6px;">
                <b style="color:#4A90D9;">{my_info['name']}</b>
                <span style="margin:0 8px;color:#ccc;">×</span>
                <b style="color:#E05C8A;">{partner_name}</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ─── 궁합 요약 카드 ───────────────────────────────
    st.markdown(
        f"""
        <div style="background:linear-gradient(135deg,#667eea22,#764ba222);border:1px solid #c7d2fe;border-radius:20px;padding:22px;margin:16px 0;">
            <div style="font-size:17px;color:#2d2d2d;line-height:1.7;">{ai_result.get('summary', '')}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ─── Why? 접기 펼치기 ─────────────────────────────
    with st.expander("🤔 왜 이런 궁합인가? 자세한 분석 보기"):
        st.markdown(f"**✨ 오행으로 보는 관계**\n\n{ai_result.get('chemistry', '')}")
        st.markdown("---")
        st.markdown(f"**💬 관계 팁**\n\n{ai_result.get('relationship_tip', '')}")

    st.markdown("---")

    # ─── 원국 + 오행 ─────────────────────────────────
    if match_type in ["친구", "연인"]:
        col1, col2 = st.columns(2)
        with col1:
            render_pillar_table(my_info["name"], my_saju["pillars"], accent_color="#4A90D9")
            render_five_elements_bar(my_info["name"], my_saju["five_elements"], accent_color="#4A90D9")

        with col2:
            render_pillar_table(partner_name, partner_saju["pillars"], accent_color="#E05C8A")
            render_five_elements_bar(partner_name, partner_saju["five_elements"], accent_color="#E05C8A")

    else:
        col1, col2 = st.columns(2)
        with col1:
            render_pillar_table(my_info["name"], my_saju["pillars"], accent_color="#4A90D9")
            render_five_elements_bar(my_info["name"], my_saju["five_elements"], accent_color="#4A90D9")

        with col2:
            render_pillar_table(partner_name, partner_saju["pillars"], accent_color="#E05C8A")
            render_five_elements_bar(partner_name, partner_saju["five_elements"], accent_color="#E05C8A")


    st.markdown("---")

    # ─── 오행 추천 ────────────────────────────────────
    st.markdown("### 🌟 오행 보완 추천")
    st.markdown(
        "<div style='font-size:14px;color:#666;margin-bottom:16px;'>"
        "부족한 오행을 채우면 관계가 더 풍성해질 수 있어요."
        "</div>",
        unsafe_allow_html=True
    )

    if match_type in ["친구", "연인"]:
        col1, col2 = st.columns(2)
        with col1:
            render_element_recommendation(
                my_info["name"],
                match_result["my_lacking_elements"],
                match_type,
                is_idol_partner=False
            )
            st.markdown(
                f"<div style='font-size:13px;color:#888;padding:0 4px;'>{ai_result.get('my_lacking_elements_comment', '')}</div>",
                unsafe_allow_html=True
            )
        with col2:
            render_element_recommendation(
                partner_name,
                match_result["partner_lacking_elements"],
                match_type,
                is_idol_partner=False
            )
            st.markdown(
                f"<div style='font-size:13px;color:#888;padding:0 4px;'>{ai_result.get('partner_lacking_elements_comment', '')}</div>",
                unsafe_allow_html=True
            )
    else:
        render_element_recommendation(
            "나",
            match_result["my_lacking_elements"],
            match_type,
            is_idol_partner=True
        )
        st.markdown(
            f"<div style='font-size:13px;color:#888;padding:0 4px;margin-top:-8px;'>{ai_result.get('my_lacking_elements_comment', '')}</div>",
            unsafe_allow_html=True
        )

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("처음으로", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    with col2:
        if st.button("다시 입력", use_container_width=True):
            st.session_state.step = "my_info"
            st.rerun()


# ─── 라우터 ──────────────────────────────────────────
init_state()
step = st.session_state.step

if step == "home":
    render_home()
elif step == "my_info":
    render_my_info()
elif step == "match_type":
    render_match_type()
elif step == "partner_info":
    render_partner_info()
elif step == "result":
    render_result()
