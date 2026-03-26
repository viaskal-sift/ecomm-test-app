import streamlit as st

import re

from business.action_logger import log_action
from business.auth import require_login
from business.cart import clear_cart
from business.order import save_order
from ui.nav import go_to
from ui.sidebar import render_cart_sidebar
from ui.utils import format_money


def _valid_expiry(value: str) -> bool:
    if not re.fullmatch(r"(0[1-9]|1[0-2])/\d{2}", value):
        return False
    month, year = int(value[:2]), int(value[3:])
    from datetime import date
    today = date.today()
    exp = date(2000 + year, month, 1)
    return exp >= date(today.year, today.month, 1)


def render_checkout() -> None:
    require_login()
    render_cart_sidebar()
    st.title("Checkout")

    order = st.session_state.active_order
    if not order:
        st.warning("No active order. Place an order first.")
        if st.button("Back to shop"):
            go_to("shop")
        return

    pricing = order["pricing"]
    items = order["items"]

    st.subheader(f"Order #{order['order_id']}")
    st.write(f"Customer: {order['shipping']['full_name']}")
    st.write(f"Ship to: {order['shipping']['address_line1']}, {order['shipping']['city']}")

    st.divider()
    st.subheader("Items")
    for item in items:
        st.write(
            f"- {item['name']} (qty {item['qty']}): {format_money(item['price'] * item['qty'])}"
        )

    st.divider()
    st.subheader("Price breakdown")
    st.write(f"Subtotal: {format_money(pricing['subtotal'])}")
    st.write(f"Tax ({pricing['tax_rate']*100:.1f}%): {format_money(pricing['tax'])}")
    st.write(f"Shipping: {format_money(pricing['shipping'])}")
    st.write(f"Total: {format_money(pricing['total'])}")

    with st.form("confirm_checkout_form"):
        st.subheader("Pay with credit card")
        cardholder_name = st.text_input("Cardholder Name", value="John Smith")
        card_number = st.text_input("Card Number", value="1234123412341234", max_chars=16)
        exp_col, cvv_col = st.columns([1, 1])
        expiration_date = exp_col.text_input("Expiration Date (MM/YY)", value="10/27", max_chars=5)
        cvv = cvv_col.text_input("CVV/CVC", placeholder="123", max_chars=3, type="password")
        agree = st.checkbox("I agree to the demo terms (no real charge).", value=False)
        submit = st.form_submit_button("Confirm order")

    if submit:
        errors = []
        if not cardholder_name.strip():
            errors.append("Cardholder Name is required.")
        if not card_number.strip().isdigit() or len(card_number.strip()) != 16:
            errors.append("Card Number must be exactly 16 digits.")
        if not _valid_expiry(expiration_date.strip()):
            errors.append("Expiration Date must be in MM/YY format.")
        if not cvv.strip().isdigit() or len(cvv.strip()) != 3:
            errors.append("CVV/CVC must be exactly 3 digits.")
        if not agree:
            errors.append("Please check the agreement box to confirm.")
        if errors:
            for e in errors:
                st.error(e)
            return

        st.session_state.active_order["payment_method"] = "Credit card"
        st.session_state.active_order["status"] = "confirmed"
        save_order(st.session_state.active_order)
        log_action("checkout", st.session_state.username, {
            "order_id": st.session_state.active_order["order_id"],
            "total": st.session_state.active_order["pricing"]["total"],
            "payment_method": "Credit card",
        })

        clear_cart()
        go_to("order_done")
