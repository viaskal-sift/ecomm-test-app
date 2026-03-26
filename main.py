import streamlit as st

from session import ensure_session_state
from ui.nav import go_to


def main() -> None:
    ensure_session_state()

    pages = {
        "login":       st.Page("pages/login.py",       title="Login",           url_path="login"),
        "shop":        st.Page("pages/shop.py",         title="Shop",            url_path="shop"),
        "cart":        st.Page("pages/cart.py",         title="Cart",            url_path="cart"),
        "checkout":    st.Page("pages/checkout.py",     title="Checkout",        url_path="checkout"),
        "order_done":  st.Page("pages/order_done.py",   title="Order Confirmed", url_path="order-done"),
        "actions_log": st.Page("pages/logs.py",         title="Actions Log",     url_path="logs"),
    }
    st.session_state.pages = pages

    pg = st.navigation(list(pages.values()), position="hidden")

    # Identify the current page key before running it.
    current_page = next((k for k, v in pages.items() if v == pg), None)

    pg.run()

    # Render the Logs button at the bottom right on every page except the logs page.
    if current_page != "actions_log":
        _, btn_col = st.columns([6, 1])
        with btn_col:
            if st.button("Logs"):
                st.session_state.previous_page = current_page
                go_to("actions_log")


main()
