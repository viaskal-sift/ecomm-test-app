import streamlit as st

from business.action_logger import log_action
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
        from ui.nav import go_to
        go_to("login")


def logout() -> None:
    log_action("logout", st.session_state.username)
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.active_order = None
    clear_cart()
    from ui.nav import go_to
    go_to("login")
