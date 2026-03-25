import streamlit as st

from business.cart import clear_cart
from db.database import get_db, hash_password


def authenticate_user(username: str, password: str) -> bool:
    conn = get_db()
    row = conn.execute(
        "SELECT 1 FROM users WHERE username = ? AND password_hash = ?",
        (username, hash_password(password)),
    ).fetchone()
    return row is not None


def require_login() -> None:
    if not st.session_state.logged_in:
        st.session_state.page = "login"


def logout() -> None:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.page = "login"
    st.session_state.active_order = None
    clear_cart()
