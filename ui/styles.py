import streamlit as st


def inject_global_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* 전체 배경 */
    .stApp {
        background: linear-gradient(160deg, #0f0a1e 0%, #1a0a3c 40%, #2d1b69 100%);
        min-height: 100vh;
    }

    .block-container {
        max-width: 480px !important;
        padding: 0 16px 80px 16px !important;
    }

    /* ── 버튼 ── */
    .stButton > button {
        border-radius: 14px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        padding: 12px 20px !important;
        border: none !important;
        transition: all 0.2s ease !important;
        letter-spacing: 0.02em !important;
        background: linear-gradient(135deg, #7c3aed, #a855f7) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(124,58,237,0.4) !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #6d28d9, #9333ea) !important;
        box-shadow: 0 6px 20px rgba(124,58,237,0.5) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* ── 텍스트 인풋 ── */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.08) !important;
        border: 1.5px solid rgba(167,139,250,0.35) !important;
        border-radius: 12px !important;
        color: #1a1a2e !important;
        font-size: 15px !important;
        padding: 12px 14px !important;
        caret-color: #a78bfa !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #a78bfa !important;
        box-shadow: 0 0 0 3px rgba(167,139,250,0.2) !important;
        color: #1a1a2e !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: rgba(167,139,250,0.4) !important;
    }

    /* ── 셀렉트박스 ── */
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.08) !important;
        border: 1.5px solid rgba(167,139,250,0.35) !important;
        border-radius: 12px !important;
        color: #ddd6fe !important;
    }
    /* 선택된 옵션 텍스트 */
    .stSelectbox > div > div > div[data-baseweb="select"] span,
    .stSelectbox > div > div span {
        color: #ddd6fe !important;
        font-weight: 500 !important;
    }
    /* 드롭다운 메뉴 */
    [data-baseweb="popover"] li {
        background: #1a0a3c !important;
        color: #ddd6fe !important;
    }
    [data-baseweb="popover"] li:hover {
        background: rgba(124,58,237,0.3) !important;
        color: white !important;
    }
    .stSelectbox svg { fill: #a78bfa !important; }

    /* ── 날짜 인풋 ── */
    .stDateInput > div > div > input {
        background: rgba(255,255,255,0.08) !important;
        border: 1.5px solid rgba(167,139,250,0.35) !important;
        border-radius: 12px !important;
        color: #1a1a2e !important;
        font-size: 15px !important;
    }

    /* ── 라디오 ── */
    .stRadio > div[role="radiogroup"] {
        gap: 10px !important;
        display: flex !important;
        flex-direction: column !important;
    }
    /* 라디오 각 옵션 카드 */
    .stRadio > div[role="radiogroup"] > label {
        background: rgba(255,255,255,0.07) !important;
        border: 1.5px solid rgba(167,139,250,0.25) !important;
        border-radius: 14px !important;
        padding: 14px 18px !important;
        color: #ddd6fe !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.18s ease !important;
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
        margin: 0 !important;
    }
    .stRadio > div[role="radiogroup"] > label:hover {
        border-color: #a78bfa !important;
        background: rgba(124,58,237,0.2) !important;
        color: white !important;
    }
    /* 선택된 라디오 */
    .stRadio > div[role="radiogroup"] > label:has(input:checked) {
        border-color: #a78bfa !important;
        background: rgba(124,58,237,0.3) !important;
        color: white !important;
        box-shadow: 0 0 0 2px rgba(167,139,250,0.3) !important;
    }
    /* 라디오 동그라미 색 */
    .stRadio input[type="radio"] { accent-color: #a78bfa !important; }

    /* ── 체크박스 ── */
    .stCheckbox > label {
        color: #c4b5fd !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
        transition: color 0.15s ease !important;
        gap: 10px !important;
    }
    .stCheckbox > label:hover {
        color: #ede9fe !important;
    }
    /* 체크박스 내부 span (실제 텍스트) 강제 연보라 */
    .stCheckbox > label > div,
    .stCheckbox > label > span,
    .stCheckbox p {
        color: #c4b5fd !important;
        font-size: 15px !important;
        font-weight: 600 !important;
    }
    .stCheckbox input[type="checkbox"] {
        accent-color: #7c3aed !important;
        width: 17px !important;
        height: 17px !important;
        cursor: pointer !important;
    }

    /* ── 모든 라벨 ── */
    label[data-testid="stWidgetLabel"],
    .stTextInput label,
    .stSelectbox label,
    .stDateInput label,
    .stRadio label[data-testid="stWidgetLabel"],
    .stCheckbox label[data-testid="stWidgetLabel"] {
        color: #a78bfa !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
        margin-bottom: 6px !important;
    }

    /* ── expander ── */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.06) !important;
        border-radius: 12px !important;
        color: #ddd6fe !important;
        font-weight: 600 !important;
        border: 1px solid rgba(167,139,250,0.2) !important;
    }
    .streamlit-expanderContent {
        background: rgba(255,255,255,0.04) !important;
        border-radius: 0 0 12px 12px !important;
        color: rgba(255,255,255,0.85) !important;
        border: 1px solid rgba(167,139,250,0.15) !important;
        border-top: none !important;
        padding: 16px !important;
    }

    /* ── 기타 ── */
    hr { border-color: rgba(167,139,250,0.15) !important; margin: 16px 0 !important; }
    .stAlert { border-radius: 12px !important; }
    .stSpinner > div { border-top-color: #a78bfa !important; }
    #MainMenu, footer, header { visibility: hidden; }

    /* 마크다운 텍스트 기본 색 */
    .stMarkdown p, .stMarkdown div { color: rgba(255,255,255,0.85); }
    </style>
    """, unsafe_allow_html=True)