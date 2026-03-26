import streamlit as st

from business.action_logger import log_action
from business.auth import authenticate_user
from ui.nav import go_to


def render_login() -> None:
    st.title("Welcome to Amazon Replacement")
    st.subheader("Sign in")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        if not username.strip() or not password.strip():
            st.error("Please enter a username and password.")
            return
        if not authenticate_user(username.strip(), password):
            st.error("Invalid username or password.")
            return
        st.session_state.logged_in = True
        st.session_state.username = username.strip()
        log_action("login", username.strip())
        go_to("shop")
