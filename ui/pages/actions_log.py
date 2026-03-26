import streamlit as st

from db.database import get_db
from ui.nav import go_to


def render_actions_log() -> None:
    back_col, _ = st.columns([1, 6])
    with back_col:
        if st.button("Back"):
            go_to(st.session_state.get("previous_page", "shop"))

    st.title("Actions Log")

    conn = get_db()
    rows = conn.execute(
        """
        SELECT created_at, username, action, details
        FROM user_actions_log
        ORDER BY created_at DESC
        """
    ).fetchall()

    if not rows:
        st.info("No actions have been logged yet.")
        return

    st.dataframe(
        [dict(row) for row in rows],
        column_config={
            "created_at": st.column_config.TextColumn("Timestamp"),
            "username":   st.column_config.TextColumn("User"),
            "action":     st.column_config.TextColumn("Action"),
            "details":    st.column_config.TextColumn("Details"),
        },
        use_container_width=True,
        hide_index=True,
    )
