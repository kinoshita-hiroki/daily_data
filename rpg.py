import streamlit as st

from game.battle import (
    SKILLS,
    check_battle_end,
    use_skill,
)
from game.state import create_battle_state

st.title("⚔️ 4人パーティバトル")

# 初期化
if "battle" not in st.session_state:
    st.session_state.battle = create_battle_state()

battle = st.session_state.battle
party = battle["party"]
enemy = battle["enemy"]

# 敵状態表示
st.subheader(f"敵：{enemy['name']}")
st.write(f"HP: {enemy['hp']} / {enemy['max_hp']}")

if enemy["hp"] > 0:
    boss_hp_rate = enemy["hp"] / enemy["max_hp"]
else:
    boss_hp_rate = 0
st.progress(boss_hp_rate)
st.divider()


# パーティ状態表示
for i, m in enumerate(party):
    marker = "▶" if i == battle["turn"] and m["hp"] > 0 else "  "
    st.write(
        f"{marker} {m['name']} "
        f"HP:{m['hp']}/{m['max_hp']} "
        f"MP:{m['mp']}/{m['max_mp']}"
    )

st.divider()


# コマンド
if not battle["finished"]:
    actor = party[battle["turn"]]

    if actor["hp"] <= 0:
        battle["log"].append(f"{actor['name']}は倒れている…")
        battle["turn"] += 1
        st.rerun()

    st.subheader(f"▶ {actor['name']} のターン")
    for skill_key in actor["skills"]:
        skill = SKILLS[skill_key]
        print(skill)

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

st.divider()
# ログ表示
for msg in battle["log"][-8:]:
    st.write(msg)


