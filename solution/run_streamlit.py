import streamlit as st

from solution.board import Compass, Move
from solution.streamlit_game import StreamlitGame

st.set_page_config(page_title="Adventure Game", layout="wide")

game = StreamlitGame()

st.title("🏹 Adventure Game")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("Status")
    st.metric("Score", st.session_state.score)

    # Compass Display
    st.subheader("Compass")
    compass_dir = st.session_state.board.get_compass_direction()

    # Simple visual representation of compass
    compass_icons = {
        Compass.NORTH: "⬆️ North",
        Compass.NORTH_EAST: "↗️ North East",
        Compass.EAST: "➡️ East",
        Compass.SOUTH_EAST: "↘️ South East",
        Compass.SOUTH: "⬇️ South",
        Compass.SOUTH_WEST: "↙️ South West",
        Compass.WEST: "⬅️ West",
        Compass.NORTH_WEST: "↖️ North West",
        Compass.HERE: "📍 You are at the Exit!"
    }
    st.info(f"Direction to Exit: **{compass_icons.get(compass_dir, 'Unknown')}**")

    # Reset Button
    if st.button("Reset Game"):
        game.reset()
        st.rerun()

with col2:
    st.header("Controls")

    # Grid for buttons
    c1, c2, c3 = st.columns(3)
    with c2:
        if st.button("North", use_container_width=True, disabled=st.session_state.finished):
            game.move(Move.NORTH)
            st.rerun()

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("West", use_container_width=True, disabled=st.session_state.finished):
            game.move(Move.WEST)
            st.rerun()
    with c3:
        if st.button("East", use_container_width=True, disabled=st.session_state.finished):
            game.move(Move.EAST)
            st.rerun()

    c1, c2, c3 = st.columns(3)
    with c2:
        if st.button("South", use_container_width=True, disabled=st.session_state.finished):
            game.move(Move.SOUTH)
            st.rerun()

    st.header("Game Log")
    # Display last 10 messages in reverse order
    for msg in reversed(st.session_state.messages[-10:]):
        st.write(msg)