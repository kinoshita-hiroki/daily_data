import streamlit as st

from game.level_up import apply_weekly_exp
from game.state import JOB_GROWTH


def confirm_weekly_growth(player_id, gained_exp):
    battle = st.session_state["battle"]
    player = battle["party"][player_id]
    role = player["name"]
    st.session_state.confirmed_roles.add(role)
    if gained_exp <= 0:
        return 0

    growth = JOB_GROWTH[player["name"]]
    new_player, level_ups = apply_weekly_exp(player, growth, gained_exp)
    battle["party"][player_id] = new_player
    st.session_state["battle"] = battle 
    return level_ups
