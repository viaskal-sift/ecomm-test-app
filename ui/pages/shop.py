import streamlit as st

from business.cart import add_to_cart
from business.catalog import product_catalog
from ui.sidebar import render_cart_sidebar
from ui.utils import format_money


def render_shop() -> None:
    st.title("Shop")
    st.caption("Add items to cart and place an order. Everything runs in memory.")

    render_cart_sidebar()

    catalog = product_catalog()
    cols = st.columns(2)
    for i, product in enumerate(catalog):
        with cols[i % 2]:
            if product.get("image_url"):
                st.image(product["image_url"], use_container_width=True)
            st.subheader(product["name"])
            st.write(f"Price: {format_money(product['price'])}")
            st.write(f"SKU: `{product['id']}`")
            st.button(
                "Add to cart",
                type="primary",
                key=f"add_{product['id']}",
                on_click=add_to_cart,
                args=(product,),
            )
