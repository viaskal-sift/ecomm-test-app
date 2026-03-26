import streamlit as st


def render_top_nav() -> None:
    _, btn_col = st.columns([8, 1])
    with btn_col:
        if st.button("📋 Actions Log"):
            st.session_state.page = "actions_log"
            st.rerun()
