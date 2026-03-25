import streamlit as st

from session import ensure_session_state
from ui.pages.login import render_login
from ui.pages.shop import render_shop
from ui.pages.place_order import render_place_order
from ui.pages.checkout import render_checkout
from ui.pages.order_done import render_order_done


def main() -> None:
    ensure_session_state()

    page = st.session_state.page

    if page == "login":
        render_login()
    elif page == "shop":
        render_shop()
    elif page == "place_order":
        render_place_order()
    elif page == "checkout":
        render_checkout()
    elif page == "order_done":
        render_order_done()
    else:
        # Fallback: recover to shop.
        st.session_state.page = "shop"
        st.rerun()


# Streamlit runs this file top-to-bottom, so we call `main()` at import time.
main()
