import uuid

import streamlit as st

from business.auth import require_login
from business.cart import cart_subtotal
from business.order import compute_order_totals
from ui.sidebar import render_cart_sidebar


def render_place_order() -> None:
    require_login()
    render_cart_sidebar()
    st.title("Place order")

    if not st.session_state.cart:
        st.warning("Your cart is empty.")
        if st.button("Back to shop"):
            st.session_state.page = "shop"
            st.rerun()
        return

    subtotal = cart_subtotal()
    totals = compute_order_totals(subtotal)

    with st.form("place_order_form"):
        st.write("Shipping details")
        full_name = st.text_input("Full name", value="John Smith")
        phone = st.text_input("Phone", value="1-415-555-6041")
        address_line1 = st.text_input("Address line 1", value="2100 Main Street")
        address_line2 = st.text_input("Address line 2 (optional)")
        city = st.text_input("City", value="New London")
        state = st.text_input("State/Province", value="New Hampshire")
        postal_code = st.text_input("Postal code", value="03257")
        country = st.text_input("Country", value="US")

        st.divider()
        st.write("Order notes (optional)")
        order_notes = st.text_area("Notes")

        submit = st.form_submit_button("Continue to checkout")

    if submit:
        required = {
            "Full name": full_name,
            "Phone": phone,
            "Address line 1": address_line1,
            "City": city,
            "State/Province": state,
            "Postal code": postal_code,
            "Country": country,
        }
        missing = [label for label, val in required.items() if not val.strip()]
        if missing:
            st.error(f"Missing required fields: {', '.join(missing)}")
            return

        order_id = str(uuid.uuid4())[:8]
        st.session_state.active_order = {
            "order_id": order_id,
            "username": st.session_state.username,
            "items": list(st.session_state.cart),
            "shipping": {
                "full_name": full_name.strip(),
                "phone": phone.strip(),
                "address_line1": address_line1.strip(),
                "address_line2": address_line2.strip(),
                "city": city.strip(),
                "state": state.strip(),
                "postal_code": postal_code.strip(),
                "country": country.strip(),
            },
            "notes": order_notes.strip(),
            "pricing": {
                "subtotal": subtotal,
                "tax_rate": totals["tax_rate"],
                "tax": totals["tax"],
                "shipping": totals["shipping"],
                "total": totals["total"],
            },
        }
        st.session_state.page = "checkout"
        st.rerun()

    st.info(
        "This is a demo order form. No payment processing occurs; checkout just confirms your order."
    )
