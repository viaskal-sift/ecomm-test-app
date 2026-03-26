import json

from db.database import get_db


def log_action(action: str, username: str | None, details: dict | None = None) -> None:
    if not username:
        return
    conn = get_db()
    row = conn.execute(
        "SELECT id FROM users WHERE username = ?", (username,)
    ).fetchone()
    user_id = row["id"] if row else None
    conn.execute(
        """
        INSERT INTO user_actions_log (user_id, username, action, details)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, username, action, json.dumps(details) if details else None),
    )
    conn.commit()
