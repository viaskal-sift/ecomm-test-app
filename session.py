import streamlit as st


def ensure_session_state() -> None:
    st.session_state.setdefault("page", "login")
    st.session_state.setdefault("logged_in", False)
    st.session_state.setdefault("username", None)
    st.session_state.setdefault("cart", [])  # list of {"id","name","price","qty"}
    st.session_state.setdefault("active_order", None)  # dict
