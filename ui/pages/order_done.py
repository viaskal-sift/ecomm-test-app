import streamlit as st

from business.auth import logout, require_login
from ui.sidebar import render_cart_sidebar
from ui.utils import format_money


def render_order_done() -> None:
    require_login()
    render_cart_sidebar()
    st.title("Order confirmed")

    order = st.session_state.active_order
    if not order:
        st.warning("No active order found.")
        return

    st.success(f"Thanks! Your order #{order['order_id']} is confirmed.")
    st.write(f"Total charged (demo): {format_money(order['pricing']['total'])}")
    st.write(f"Payment method: {order.get('payment_method')}")

    if st.button("Back to shop"):
        st.session_state.page = "shop"
        st.rerun()

    if st.button("Start fresh"):
        st.session_state.active_order = None
        logout()
        st.rerun()
