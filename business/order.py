from db.database import get_db


def compute_order_totals(subtotal: float) -> dict:
    # Fixed demo tax/shipping; tweak as desired.
    tax_rate = 0.075
    shipping = 6.99 if subtotal > 0 else 0.0
    tax = subtotal * tax_rate
    total = subtotal + tax + shipping
    return {"tax_rate": tax_rate, "shipping": shipping, "tax": tax, "total": total}


def save_order(order: dict) -> None:
    """Persist a confirmed order (and its items) to the in-memory DB."""
    conn = get_db()
    s = order["shipping"]
    p = order["pricing"]

    conn.execute(
        """
        INSERT OR REPLACE INTO orders (
            order_id, username, status, payment_method, notes,
            subtotal, tax_rate, tax, shipping, total,
            shipping_full_name, shipping_phone,
            shipping_address1, shipping_address2,
            shipping_city, shipping_state,
            shipping_postal_code, shipping_country
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            order["order_id"],
            order["username"],
            order.get("status", "confirmed"),
            order.get("payment_method"),
            order.get("notes", ""),
            p["subtotal"], p["tax_rate"], p["tax"], p["shipping"], p["total"],
            s["full_name"], s["phone"],
            s["address_line1"], s.get("address_line2", ""),
            s["city"], s["state"],
            s["postal_code"], s["country"],
        ),
    )

    conn.executemany(
        """
        INSERT INTO order_items (order_id, product_id, name, price, qty)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (order["order_id"], item["id"], item["name"], item["price"], item["qty"])
            for item in order["items"]
        ],
    )

    conn.commit()


def get_order(order_id: str) -> dict | None:
    """Retrieve a persisted order with its items from the DB."""
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM orders WHERE order_id = ?", (order_id,)
    ).fetchone()
    if not row:
        return None

    items = conn.execute(
        "SELECT product_id, name, price, qty FROM order_items WHERE order_id = ?",
        (order_id,),
    ).fetchall()

    return {**dict(row), "items": [dict(i) for i in items]}
