# state.py
import streamlit as st

from game.state import create_battle_state


def init_state():
    if "battle" not in st.session_state:
        st.session_state.battle = create_battle_state()

    if "confirmed_roles" not in st.session_state:
        st.session_state.confirmed_roles = set()
