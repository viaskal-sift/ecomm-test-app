import streamlit as st

from business.cart import cart_item_count, cart_subtotal, clear_cart, update_cart_qty
from ui.utils import format_money


def render_cart_sidebar() -> None:
    st.sidebar.title("Cart")
    if not st.session_state.cart:
        st.sidebar.caption("Your cart is empty.")
    else:
        st.sidebar.caption(f"{cart_item_count()} item(s)")
        st.sidebar.divider()
        for item in st.session_state.cart:
            thumb_col, info_col = st.sidebar.columns([1, 3])
            if item.get("image_url"):
                thumb_col.image(item["image_url"], width=60)
            info_col.write(f"**{item['name']}**")
            info_col.write(f"{format_money(item['price'])}  ×  {item['qty']}")

            c_minus, c_plus = st.sidebar.columns([1, 1])
            c_minus.button(
                "-",
                key=f"qty_minus_{item['id']}",
                on_click=update_cart_qty,
                args=(item["id"], -1),
            )
            c_plus.button(
                "+",
                key=f"qty_plus_{item['id']}",
                on_click=update_cart_qty,
                args=(item["id"], 1),
            )
            st.sidebar.write("---")

    st.sidebar.divider()
    st.sidebar.write(f"Subtotal: {format_money(cart_subtotal())}")
    st.sidebar.write(f"Total items: {cart_item_count()}")

    if st.sidebar.button("Clear cart", disabled=not st.session_state.cart):
        clear_cart()
        st.rerun()

    if st.sidebar.button(
        "Place order",
        disabled=not st.session_state.cart,
        help="Start checkout and enter shipping details.",
    ):
        st.session_state.page = "place_order"
        st.rerun()

    if st.session_state.logged_in and st.sidebar.button("Logout"):
        from business.auth import logout
        logout()
        st.rerun()
