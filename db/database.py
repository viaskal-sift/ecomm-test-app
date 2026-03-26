import atexit
import hashlib
import sqlite3

import streamlit as st


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


@st.cache_resource
def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    _create_schema(conn)
    _seed_data(conn)
    atexit.register(conn.close)
    return conn


def _create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS products (
            id        TEXT PRIMARY KEY,
            name      TEXT NOT NULL,
            price     REAL NOT NULL,
            image_url TEXT
        );

        CREATE TABLE IF NOT EXISTS orders (
            order_id             TEXT PRIMARY KEY,
            username             TEXT NOT NULL,
            status               TEXT NOT NULL DEFAULT 'confirmed',
            payment_method       TEXT,
            notes                TEXT,
            subtotal             REAL NOT NULL,
            tax_rate             REAL NOT NULL,
            tax                  REAL NOT NULL,
            shipping             REAL NOT NULL,
            total                REAL NOT NULL,
            shipping_full_name   TEXT NOT NULL,
            shipping_phone       TEXT NOT NULL,
            shipping_address1    TEXT NOT NULL,
            shipping_address2    TEXT,
            shipping_city        TEXT NOT NULL,
            shipping_state       TEXT NOT NULL,
            shipping_postal_code TEXT NOT NULL,
            shipping_country     TEXT NOT NULL,
            created_at           TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS order_items (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id   TEXT NOT NULL REFERENCES orders(order_id),
            product_id TEXT NOT NULL,
            name       TEXT NOT NULL,
            price      REAL NOT NULL,
            qty        INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS user_actions_log (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER REFERENCES users(id),
            username   TEXT NOT NULL,
            action     TEXT NOT NULL CHECK(action IN (
                           'login', 'logout', 'add_to_cart',
                           'remove_from_cart', 'create_order', 'checkout'
                       )),
            details    TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
    """)
    conn.commit()


def _seed_data(conn: sqlite3.Connection) -> None:
    users = [
        ("john", hash_password("123")),
    ]
    conn.executemany(
        "INSERT OR IGNORE INTO users (username, password_hash) VALUES (?, ?)",  # id is AUTOINCREMENT
        users,
    )

    products = [
        (
            "sku-tee-001",
            "Everyday Tee",
            19.99,
            "https://placehold.co/400x300/dbeafe/1e40af?text=Everyday+Tee",
        ),
        (
            "sku-mug-002",
            "Ceramic Mug",
            12.50,
            "https://placehold.co/400x300/fef3c7/92400e?text=Ceramic+Mug",
        ),
        (
            "sku-socks-003",
            "Comfy Socks (3-pack)",
            21.00,
            "https://placehold.co/400x300/dcfce7/166534?text=Comfy+Socks",
        ),
        (
            "sku-bottle-004",
            "Insulated Bottle",
            29.95,
            "https://placehold.co/400x300/e0f2fe/075985?text=Insulated+Bottle",
        ),
    ]
    conn.executemany(
        "INSERT OR IGNORE INTO products (id, name, price, image_url) VALUES (?, ?, ?, ?)",
        products,
    )
    conn.commit()
