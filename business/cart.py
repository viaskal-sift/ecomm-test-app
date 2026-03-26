import streamlit as st

from business.action_logger import log_action


def cart_subtotal() -> float:
    return sum(item["price"] * item["qty"] for item in st.session_state.cart)


def cart_item_count() -> int:
    return sum(item["qty"] for item in st.session_state.cart)


def add_to_cart(product: dict) -> None:
    cart = st.session_state.cart
    for item in cart:
        if item["id"] == product["id"]:
            item["qty"] += 1
            st.session_state.cart = cart
            log_action("add_to_cart", st.session_state.username, {
                "product_id": product["id"], "name": product["name"], "price": product["price"],
            })
            return
    cart.append(
        {
            "id": product["id"],
            "name": product["name"],
            "price": product["price"],
            "image_url": product.get("image_url"),
            "qty": 1,
        }
    )
    st.session_state.cart = cart
    log_action("add_to_cart", st.session_state.username, {
        "product_id": product["id"], "name": product["name"], "price": product["price"],
    })


def update_cart_qty(product_id: str, delta: int) -> None:
    cart = st.session_state.cart
    for item in cart:
        if item["id"] == product_id:
            item["qty"] += delta
            if item["qty"] <= 0:
                cart.remove(item)
            st.session_state.cart = cart
            if delta < 0:
                log_action("remove_from_cart", st.session_state.username, {
                    "product_id": product_id,
                })
            return


def clear_cart() -> None:
    st.session_state.cart = []
