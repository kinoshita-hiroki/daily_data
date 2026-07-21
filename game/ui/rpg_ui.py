from typing import Optional

import streamlit as st

from game.domain.models.battle import Battle
from game.domain.models.character import Character
from game.domain.models.player import Player
from game.domain.skills.skill import Skill
from game.services.battle_service import BattleService
from game.session_state import init_state
from game.ui.review_ui import render_level_up


def render_rpg_page():
    st.title("⚔️ 4人パーティバトル")

    # 初期化
    init_state()

    battle = st.session_state.battle

    BattleService.update(battle)

    render_enemy_state(battle)
    st.divider()
    render_party_state(battle)
    st.divider()

    render_command(battle)
    st.divider()

    render_log(battle)
    st.divider()
    render_level_up(battle)

def render_enemy_state(battle):
    for enemy in battle.enemies:
        # 敵状態表示
        st.subheader(f"敵：{enemy.name}")
        st.write(f"HP: {int(enemy.stats.hp)} / {int(enemy.stats.max_hp)}")

        if enemy.stats.hp > 0:
            boss_hp_rate = enemy.stats.hp / enemy.stats.max_hp
        else:
            boss_hp_rate = 0
        st.progress(boss_hp_rate)

def render_party_state(battle):
    for player in battle.players:
        marker = "▶" if player == battle.current_actor() else "  "
        st.write(
            f"{marker} {player.name} "
            f"HP:{int(player.stats.hp)}/{int(player.stats.max_hp)} "
            f"MP:{int(player.stats.mp)}/{int(player.stats.max_mp)}"
        )

def render_log(battle):
    for msg in battle.log[-8:]:
        st.write(msg)

def skill_select_ui(player: Player) -> Skill:
    skills = player.skills  # dict[str, Skill]

    selected_name = st.radio(
        "スキルを選択",
        list(skills.keys())
    )
    return skills[selected_name]

def target_select_ui(battle: Battle, skill: Skill, actor: Player) -> Optional[Character]:
    candidates = skill.candidate_targets(actor, battle)
    names = [candidate.name for candidate in candidates]
    if len(names) == 0:
        return None

    selected_pos = st.radio(
        "対象を選択",
        range(len(candidates)),
        format_func=lambda i: names[i]
    )
    return candidates[selected_pos]

def render_battle_result(battle):
    if not battle.is_finished():
        return False

    if battle.is_victory():
        st.success("勝利！")
    elif battle.is_lose():
        st.error("敗北…")
    if st.button("🔄 もう一度"):
        del st.session_state.battle
        st.rerun()
    return True


def render_command(battle):

    if render_battle_result(battle):
        return

    actor = battle.current_actor()
    if actor is None:
        st.rerun()
        return

    st.subheader(f"▶ {actor.name} のターン")
    # ui/battle_ui.py（例）
    # ① スキル選択
    selected_skill = skill_select_ui(actor)

    # ② ターゲット選択（必要な場合のみ）
    target = None
    if selected_skill.target_type.requires_target():
        target = target_select_ui(
            battle=battle,
            skill=selected_skill,
            actor=actor
        )
    # ③ 実行

    if st.button("▶ 行動実行"):
        BattleService.execute_player_turn(battle, actor, selected_skill, target)
        st.rerun()


