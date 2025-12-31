import pandas as pd
import streamlit as st

import app.config.config as config
from game.battle import SKILLS, check_battle_end, next_turn, use_skill
from game.growth import confirm_weekly_growth


def render_enemy_state(battle):
    enemy = battle["enemy"]
    # 敵状態表示
    st.subheader(f"敵：{enemy['name']}")
    st.write(f"HP: {enemy['hp']} / {enemy['max_hp']}")

    if enemy["hp"] > 0:
        boss_hp_rate = enemy["hp"] / enemy["max_hp"]
    else:
        boss_hp_rate = 0
    st.progress(boss_hp_rate)

def render_party_state(battle):
    for i, m in enumerate(battle["party"]):
        marker = "▶" if i == battle["turn"] and m["hp"] > 0 else "  "
        st.write(
            f"{marker} {m['name']} "
            f"HP:{m['hp']}/{m['max_hp']} "
            f"MP:{m['mp']}/{m['max_mp']}"
        )

def render_log(battle):
    for msg in battle["log"][-8:]:
        st.write(msg)


def render_command(battle):
    party = battle["party"]
    if not battle["finished"]:

        actor = party[battle["turn"]]

        if actor["hp"] <= 0:
            battle["log"].append(f"{actor['name']}は倒れている…")
            next_turn(battle)
            st.rerun()

        st.subheader(f"▶ {actor['name']} のターン")
        for skill_key in actor["skills"]:
            skill = SKILLS[skill_key]

            if skill["target"] == "enemy":
                if st.button(skill["name"]):
                    use_skill(battle, skill_key, None)
                    check_battle_end(battle)
                    st.rerun()

            elif skill["target"] == "ally":
                st.write(f"🪄 {skill['name']} 対象選択")
                for i, m in enumerate(party):
                    if m["hp"] > 0:
                        if st.button(f"{skill['name']} → {m['name']}"):
                            use_skill(battle, skill_key, i)
                            check_battle_end(battle)
                            st.rerun()

    else:
        st.success("戦闘終了")
        if st.button("🔄 もう一度"):
            del st.session_state.battle
            st.rerun()

def render_review_week(character, log_csv):
    df_logs = pd.read_csv(log_csv)
    df_chara = df_logs[df_logs["character"]==character]
    total_exp = sum(df_chara["exp"])

    st.subheader("📜 今週の振り返り")

    if len(df_chara) == 0:
        st.info("今週は静かな冒険だった…")
        return 0
    st.write(f"**獲得EXP合計：{total_exp}**")
    st.dataframe(df_chara)
    return total_exp



def render_level_up(battle):
    party = battle["party"]
    st.header("🌙 週末イベント：成長の刻")
    log_csv = config.RPG_EX_CSV
    for i, player in enumerate(party):
        role = player["name"]
        if role in st.session_state.confirmed_roles:
            st.write("✅ 成長確定済み")
            continue
        gained_exp = render_review_week(role, log_csv)
        if st.button("📈 成長を確定する", key = role):
            level_ups = confirm_weekly_growth(i, gained_exp)
            level = st.session_state["battle"]["party"][i]["level"]
            if level_ups > 0:
                st.balloons()
                st.success(
                    f"🎉 {role}は {level_ups} 回レベルアップ！\n"
                    f"現在 Lv {level}"
                )
            else:
                st.info("経験は積んだが、まだ次の境地には届かなかった…")
