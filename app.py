import streamlit as st

from ui.styles import inject_global_styles
from ui.pages import init_state, render_home, render_my_info, render_match_type, render_partner_info
from ui.result_page import render_result

st.set_page_config(page_title="Saju Match", page_icon="🌙", layout="centered")
inject_global_styles()

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