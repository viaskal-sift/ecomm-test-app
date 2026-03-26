import streamlit as st


def go_to(page_name: str) -> None:
    st.switch_page(st.session_state.pages[page_name])
