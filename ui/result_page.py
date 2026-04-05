import streamlit as st

from core.calculator import calculate_saju_data
from core.ten_gods import calculate_ten_gods
from core.yearly_fortune import get_current_year_fortune
from core.prompt_builder import build_match_prompt
from core.gemini_client import generate_interpretation
from core.compatibility import calculate_match
from core.idol_lookup import find_idol

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


def render_pillar_table(name, pillars, accent_color="#7C3AED"):
    labels = {"year": "연주", "month": "월주", "day": "일주", "hour": "시주"}
    visible_keys = [k for k in ["year", "month", "day"] if k in pillars]
    if "hour" in pillars and pillars["hour"] and pillars["hour"].get("stem"):
        visible_keys.append("hour")

    cards_html = ""
    for key in visible_keys:
        p = pillars[key]
        sc = ELEMENT_COLORS[p["stem_element"]]
        bc = ELEMENT_COLORS[p["branch_element"]]
        cards_html += (
            "<div style='flex:1;min-width:0;border:1px solid rgba(196,181,253,0.3);border-radius:16px;"
            "padding:10px 8px;background:rgba(255,255,255,0.07);box-shadow:0 2px 8px rgba(124,58,237,0.12);'>"
            "<div style='font-size:11px;color:#a78bfa;text-align:center;margin-bottom:7px;font-weight:600;'>"
            "{label}</div>"
            "<div style='background:{sbg};border-radius:10px;padding:9px 6px;margin-bottom:6px;text-align:center;'>"
            "<div style='font-size:26px;font-weight:800;color:{stxt};'>{stem}</div>"
            "<div style='font-size:11px;color:{stxt};opacity:0.85;'>{stem_kr} · {stem_el}</div></div>"
            "<div style='background:{bbg};border-radius:10px;padding:9px 6px;text-align:center;'>"
            "<div style='font-size:26px;font-weight:800;color:{btxt};'>{branch}</div>"
            "<div style='font-size:11px;color:{btxt};opacity:0.85;'>{branch_kr} · {branch_el}</div>"
            "</div></div>"
        ).format(
            label=labels[key],
            sbg=sc["bg"], stxt=sc["text"], stem=p["stem"], stem_kr=p["stem_kr"], stem_el=p["stem_element"],
            bbg=bc["bg"], btxt=bc["text"], branch=p["branch"], branch_kr=p["branch_kr"], branch_el=p["branch_element"],
        )

    st.markdown(
        "<div style='margin-bottom:6px;'>"
        "<span style='font-size:12px;font-weight:700;color:{ac};padding-left:10px;"
        "border-left:3px solid {ac};letter-spacing:0.04em;'>{name}의 원국</span></div>"
        "<div style='display:flex;gap:7px;margin-bottom:14px;'>{cards}</div>".format(
            ac=accent_color, name=name, cards=cards_html),
        unsafe_allow_html=True,
    )


def render_five_elements_bar(name, five_elements, accent_color="#7C3AED"):
    total = max(sum(five_elements.values()), 1)
    bars_html = ""
    for e in ["목", "화", "토", "금", "수"]:
        val = five_elements.get(e, 0)
        pct = int(val / total * 100)
        c = ELEMENT_COLORS[e]
        bars_html += (
            "<div style='display:flex;align-items:center;gap:10px;margin-bottom:9px;'>"
            "<div style='width:32px;height:32px;border-radius:9px;background:{bg};"
            "display:flex;align-items:center;justify-content:center;flex-shrink:0;'>"
            "<span style='font-size:15px;font-weight:700;color:{txt};'>{e}</span></div>"
            "<div style='flex:1;background:rgba(196,181,253,0.15);border-radius:999px;height:14px;overflow:hidden;'>"
            "<div style='width:{pct}%;background:{bar};height:100%;border-radius:999px;'></div></div>"
            "<div style='width:22px;text-align:right;font-size:13px;font-weight:700;color:#c4b5fd;'>{val}</div>"
            "</div>"
        ).format(bg=c["bg"], txt=c["text"], e=e, pct=pct, bar=c["bar"], val=val)

    st.markdown(
        "<div style='margin-bottom:6px;'>"
        "<span style='font-size:12px;font-weight:700;color:{ac};padding-left:10px;"
        "border-left:3px solid {ac};letter-spacing:0.04em;'>{name}의 오행</span></div>"
        "<div style='background:rgba(255,255,255,0.05);border:1px solid rgba(196,181,253,0.2);border-radius:14px;"
        "padding:14px 14px 6px 14px;margin-bottom:14px;'>{bars}</div>".format(
            ac=accent_color, name=name, bars=bars_html),
        unsafe_allow_html=True,
    )


def render_element_recommendation(name, lacking, match_type, is_idol_partner=False):
    if not lacking:
        st.markdown(
            "<div style='background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.3);border-radius:14px;"
            "padding:14px;margin-bottom:14px;'>"
            "<div style='font-size:13px;color:#6ee7b7;'>✅ {name}은 오행이 균형 잡혀 있습니다.</div>"
            "</div>".format(name=name),
            unsafe_allow_html=True,
        )
        return

    badges_html = ""
    effects_html = ""
    for e in lacking:
        c = ELEMENT_COLORS[e]
        badges_html += (
            "<span style='display:inline-block;background:{bg};color:{txt};"
            "border:1px solid {txt}33;border-radius:999px;padding:3px 12px;"
            "font-size:13px;font-weight:700;margin-right:5px;margin-bottom:5px;'>{e}</span>"
        ).format(bg=c["bg"], txt=c["text"], e=e)
        effects_html += (
            "<div style='display:flex;align-items:flex-start;gap:8px;margin-top:7px;'>"
            "<div style='width:8px;height:8px;border-radius:50%;background:{txt};"
            "margin-top:5px;flex-shrink:0;'></div>"
            "<div style='font-size:13px;color:#ddd6fe;'>"
            "<b style='color:{txt};'>{e} 기운</b>을 보완하면: {eff}</div></div>"
        ).format(txt=c["text"], e=e, eff=ELEMENT_EFFECTS[e])

    goods_section = ""
    if is_idol_partner:
        goods_list = "".join([
            "<li style='margin-bottom:5px;font-size:13px;color:#ddd6fe;'>{g}</li>".format(g=ELEMENT_GOODS[e])
            for e in lacking
        ])
        goods_section = (
            "<div style='margin-top:12px;padding-top:10px;border-top:1px solid rgba(196,181,253,0.2);'>"
            "<div style='font-size:12px;font-weight:700;color:#c4b5fd;margin-bottom:7px;'>🛍️ 추천 굿즈</div>"
            "<ul style='padding-left:16px;margin:0;'>{gl}</ul></div>"
        ).format(gl=goods_list)

    label = "나에게" if name == "나" else name + "에게"
    st.markdown(
        "<div style='background:rgba(124,58,237,0.1);border:1px solid rgba(196,181,253,0.2);border-radius:14px;"
        "padding:16px;margin-bottom:14px;'>"
        "<div style='font-size:13px;font-weight:700;color:#c4b5fd;margin-bottom:9px;'>"
        "💡 {label} 부족한 오행</div>"
        "<div style='margin-bottom:7px;'>{badges}</div>"
        "{effects}{goods}</div>".format(
            label=label, badges=badges_html, effects=effects_html, goods=goods_section),
        unsafe_allow_html=True,
    )


def render_result():
    my_info = st.session_state.my_info
    partner_info = st.session_state.partner_info
    match_type = st.session_state.match_type

    with st.spinner("내 사주를 계산 중입니다..."):
        my_saju = calculate_saju_data(birth_date=my_info["birth_date"], birth_time=my_info["birth_time"])
        my_ten_gods = calculate_ten_gods(my_saju["pillars"], my_saju["day_master"])

    if match_type in ["친구", "연인"]:
        with st.spinner("상대 사주를 계산 중입니다..."):
            partner_saju = calculate_saju_data(birth_date=partner_info["birth_date"], birth_time=partner_info["birth_time"])
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
            partner_saju = calculate_saju_data(birth_date=idol["birth_date"], birth_time=idol["birth_time"])
            partner_ten_gods = calculate_ten_gods(partner_saju["pillars"], partner_saju["day_master"])
            partner_name = idol["name"]
            partner_gender = idol["gender"]

    match_result = calculate_match(my_saju["five_elements"], partner_saju["five_elements"])
    year_fortune = get_current_year_fortune()

    my_profile = {
        "name": my_info["name"], "gender": my_info["gender"],
        "birth_date": my_saju["birth_date"], "birth_time": my_saju["birth_time"],
        "pillars": my_saju["pillars"], "day_master": my_saju["day_master"],
        "day_master_kr": my_saju["day_master_kr"], "five_elements": my_saju["five_elements"],
        "ten_gods": my_ten_gods, "year_fortune": year_fortune,
    }
    partner_profile = {
        "name": partner_name, "gender": partner_gender,
        "birth_date": partner_saju["birth_date"], "birth_time": partner_saju["birth_time"],
        "pillars": partner_saju["pillars"], "day_master": partner_saju["day_master"],
        "day_master_kr": partner_saju["day_master_kr"], "five_elements": partner_saju["five_elements"],
        "ten_gods": partner_ten_gods, "year_fortune": year_fortune,
    }

    with st.spinner("AI가 관계 해석을 작성 중입니다..."):
        prompt = build_match_prompt(
            match_type=match_type, my_profile=my_profile,
            partner_profile=partner_profile, match_result=match_result,
        )
        ai_result = generate_interpretation(prompt)

    # ── 결과 헤더
    type_emoji = {"친구": "🤝", "연인": "💕", "K-pop Idol": "⭐"}
    emoji = type_emoji.get(match_type, "✨")
    st.markdown(
        "<div style='text-align:center;padding:28px 0 16px 0;'>"
        "<div style='font-size:12px;font-weight:700;color:#a78bfa;letter-spacing:0.1em;"
        "text-transform:uppercase;margin-bottom:8px;'>SAJU MATCH RESULT</div>"
        "<div style='font-size:26px;font-weight:800;color:#ede9fe;'>{emoji} {mt} 궁합</div>"
        "<div style='font-size:15px;color:#c4b5fd;margin-top:8px;'>"
        "<b style='color:#ddd6fe;'>{me}</b>"
        "<span style='margin:0 10px;color:#7c3aed;'>×</span>"
        "<b style='color:#f0abfc;'>{partner}</b>"
        "</div></div>".format(emoji=emoji, mt=match_type, me=my_info["name"], partner=partner_name),
        unsafe_allow_html=True,
    )

    # ── 점수 카드
    score = match_result["score"]
    st.markdown(
        "<div style='background:linear-gradient(135deg,#4c1d95,#7c3aed,#a855f7);"
        "border-radius:24px;padding:28px 20px;margin:0 0 20px 0;text-align:center;"
        "box-shadow:0 8px 30px rgba(124,58,237,0.4);'>"
        "<div style='font-size:52px;font-weight:900;color:white;line-height:1;'>{score}</div>"
        "<div style='font-size:14px;color:#e9d5ff;margin-top:4px;'>/ 100점</div>"
        "<div style='background:rgba(255,255,255,0.12);border-radius:12px;"
        "padding:14px 16px;margin-top:18px;text-align:left;'>"
        "<div style='font-size:14px;color:rgba(255,255,255,0.92);line-height:1.7;'>"
        "{summary}</div></div></div>".format(score=score, summary=ai_result.get("summary", "")),
        unsafe_allow_html=True,
    )

    # ── 자세한 분석 (expander) — 연보라 컨셉
    st.markdown(
        "<style>"
        ".stExpander > details > summary {"
        "  background: rgba(124,58,237,0.15) !important;"
        "  border: 1.5px solid rgba(167,139,250,0.4) !important;"
        "  border-radius: 14px !important;"
        "  color: #c4b5fd !important;"
        "  font-weight: 700 !important;"
        "  font-size: 14px !important;"
        "  padding: 14px 18px !important;"
        "}"
        ".stExpander > details > summary:hover {"
        "  background: rgba(124,58,237,0.25) !important;"
        "  color: #ede9fe !important;"
        "}"
        ".stExpander > details[open] > summary {"
        "  border-radius: 14px 14px 0 0 !important;"
        "  border-bottom: none !important;"
        "}"
        ".stExpander > details > div {"
        "  background: rgba(255,255,255,0.04) !important;"
        "  border: 1.5px solid rgba(167,139,250,0.25) !important;"
        "  border-top: none !important;"
        "  border-radius: 0 0 14px 14px !important;"
        "  color: #ddd6fe !important;"
        "}"
        ".stExpander .stMarkdown p, .stExpander .stMarkdown div {"
        "  color: #ddd6fe !important;"
        "}"
        "</style>",
        unsafe_allow_html=True,
    )
    with st.expander("🔍 자세한 분석 보기"):
        chemistry_text = "**✨ 오행으로 보는 관계**\n\n" + ai_result.get("chemistry", "")
        st.markdown(chemistry_text)
        st.markdown("---")
        tip_text = "**💬 관계 팁**\n\n" + ai_result.get("relationship_tip", "")
        st.markdown(tip_text)

    # ── 섹션 헤더
    st.markdown(
        "<div style='font-size:13px;font-weight:700;color:#a78bfa;margin:24px 0 12px 0;"
        "letter-spacing:0.05em;text-transform:uppercase;'>📊 사주 원국 & 오행 분석</div>",
        unsafe_allow_html=True,
    )

    # ── 원국: 나 위 / 상대 아래 (세로 배치)
    render_pillar_table(my_info["name"], my_saju["pillars"], "#a78bfa")
    render_pillar_table(partner_name, partner_saju["pillars"], "#f0abfc")

    # ── 오행: 좌우 나란히
    col1, col2 = st.columns(2)
    with col1:
        render_five_elements_bar(my_info["name"], my_saju["five_elements"], "#a78bfa")
    with col2:
        render_five_elements_bar(partner_name, partner_saju["five_elements"], "#f0abfc")

    # ── 오행 보완 추천
    st.markdown(
        "<div style='background:linear-gradient(135deg,rgba(124,58,237,0.15),rgba(168,85,247,0.1));"
        "border:1px solid rgba(196,181,253,0.3);border-radius:20px;padding:18px 16px 6px 16px;margin:8px 0 16px 0;'>"
        "<div style='font-size:14px;font-weight:800;color:#ddd6fe;margin-bottom:4px;'>🌟 오행 보완 추천</div>"
        "<div style='font-size:12px;color:#a78bfa;margin-bottom:12px;'>"
        "부족한 오행을 채우면 관계가 더 풍성해져요</div>",
        unsafe_allow_html=True,
    )
    if match_type in ["친구", "연인"]:
        col1, col2 = st.columns(2)
        with col1:
            render_element_recommendation(my_info["name"], match_result["my_lacking_elements"], match_type, False)
            st.markdown(
                "<div style='font-size:12px;color:#a78bfa;margin-top:-8px;'>{c}</div>".format(
                    c=ai_result.get("my_lacking_elements_comment", "")),
                unsafe_allow_html=True,
            )
        with col2:
            render_element_recommendation(partner_name, match_result["partner_lacking_elements"], match_type, False)
            st.markdown(
                "<div style='font-size:12px;color:#a78bfa;margin-top:-8px;'>{c}</div>".format(
                    c=ai_result.get("partner_lacking_elements_comment", "")),
                unsafe_allow_html=True,
            )
    else:
        render_element_recommendation("나", match_result["my_lacking_elements"], match_type, True)
        st.markdown(
            "<div style='font-size:12px;color:#a78bfa;margin-top:-8px;'>{c}</div>".format(
                c=ai_result.get("my_lacking_elements_comment", "")),
            unsafe_allow_html=True,
        )

    st.markdown("</div><div style='height:16px;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 처음으로", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    with col2:
        if st.button("✏️ 다시 입력", use_container_width=True):
            st.session_state.step = "my_info"
            st.rerun()