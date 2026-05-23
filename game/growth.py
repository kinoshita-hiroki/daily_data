import streamlit as st


def confirm_weekly_growth(player_id, gained_exp):
    battle = st.session_state["battle"]
    player = battle.players[player_id]
    name = player.name
    st.session_state.confirmed_roles.add(name)
    if gained_exp <= 0:
        return 0

    level_ups = player.apply_exp(gained_exp)
    battle.players[player_id] = player
    st.session_state["battle"] = battle 
    return level_ups
