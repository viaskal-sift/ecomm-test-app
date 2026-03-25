from db.database import get_db


def product_catalog() -> list[dict]:
    conn = get_db()
    rows = conn.execute("SELECT id, name, price, image_url FROM products ORDER BY rowid").fetchall()
    return [dict(row) for row in rows]
