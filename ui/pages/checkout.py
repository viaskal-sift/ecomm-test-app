import streamlit as st

from business.auth import require_login
from business.cart import clear_cart
from business.order import save_order
from ui.sidebar import render_cart_sidebar
from ui.utils import format_money


def render_checkout() -> None:
    require_login()
    render_cart_sidebar()
    st.title("Checkout")

    order = st.session_state.active_order
    if not order:
        st.warning("No active order. Place an order first.")
        if st.button("Back to shop"):
            st.session_state.page = "shop"
            st.rerun()
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
        st.subheader("Payment (demo)")
        payment_method = st.selectbox(
            "Payment method",
            options=["Credit card", "PayPal", "Apple Pay"],
            index=0,
        )
        agree = st.checkbox("I agree to the demo terms (no real charge).", value=False)
        submit = st.form_submit_button("Confirm order")

    if submit:
        if not agree:
            st.error("Please check the agreement box to confirm.")
            return

        st.session_state.active_order["payment_method"] = payment_method
        st.session_state.active_order["status"] = "confirmed"
        save_order(st.session_state.active_order)

        clear_cart()
        st.session_state.page = "order_done"
        st.rerun()
