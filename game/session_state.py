# state.py
import streamlit as st

from game.domain.factory.battle_factory import create_battle


def init_state():
    if "battle" not in st.session_state:
        st.session_state.battle = create_battle(["勇者", "戦士", "魔法使い", "僧侶"], ["怨霊"])

    if "confirmed_roles" not in st.session_state:
        st.session_state.confirmed_roles = set()
