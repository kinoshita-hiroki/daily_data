from typing import Optional

import altair as alt
import pandas as pd
import streamlit as st

import app.config.config as config
from game.domain.models.battle import Battle
from game.domain.models.character import Character
from game.domain.models.command import Command
from game.domain.models.player import Player
from game.domain.models.target_type import TargetType
from game.domain.skills.skill import Skill
from game.growth import confirm_weekly_growth


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
    for i, m in enumerate(battle.players):
        marker = "▶" if i == battle.turn and m.stats.hp > 0 else "  "
        st.write(
            f"{marker} {m.name} "
            f"HP:{int(m.stats.hp)}/{int(m.stats.max_hp)} "
            f"MP:{int(m.stats.mp)}/{int(m.stats.max_mp)}"
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
    if skill.target_type == TargetType.ENEMY_SINGLE:
        enemies = battle.alive_enemies()  # [Enemy, ...]

        # 表示用の名前リスト
        names = [enemy.name for enemy in enemies]

        # radio は「alive_enemies の中での位置」を返す
        selected_pos = st.radio(
            "対象を選択",
            range(len(enemies)),
            format_func=lambda i: names[i]
        )

        # 実際に返すのは battle.enemies の添字 ではなくオブジェクト
        enemy = enemies[selected_pos]
        return enemy

    if skill.target_type == TargetType.ALLY_SINGLE:
        players = battle.alive_players()  # [Player, ...]

        # 表示用の名前リスト
        names = [player.name for player in players]

        # radio は「alive_enemies の中での位置」を返す
        selected_pos = st.radio(
            "対象を選択",
            range(len(players)),
            format_func=lambda i: names[i]
        )

        # 実際に返すのは battle.enemies の添字 ではなくオブジェクト
        player = players[selected_pos]
        return player
    return None



def render_command(battle):

    if battle.is_finished():
        st.success("戦闘終了")
        if st.button("🔄 もう一度"):
            del st.session_state.battle
            st.rerun()
        return

    player_idx, actor = battle.next_actor()
    if not(actor.is_alive()):
        battle.log.append(f"{actor.name}は倒れている…")
        battle.next_turn()
        st.rerun()

    if not actor.can_act():
        # battle.log.append(f"{actor.name}は動けない！") # Effect.on_turn_start でメッセージを出している想定
        battle.next_turn()
        st.rerun()

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
        # MP不足チェック
        if not selected_skill.check_cost(actor, battle):
            st.rerun()

        command = Command(
            actor=actor,
            target=target,
            skill=selected_skill,
        )
        battle.execute(command)
        battle.check_battle_end()
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



def render_exp_charts(log_csv):
    st.subheader("📊 役割別獲得経験値の推移（7日間移動平均）")
    try:
        df = pd.read_csv(log_csv)
        if df.empty:
            st.info("データがありません")
            return

        df["date"] = pd.to_datetime(df["date"])
        # 日付とキャラクターでグループ化して日ごとの合計を算出
        df_daily = df.groupby(["date", "character"])["exp"].sum().reset_index()

        # 全ての日付とキャラクターの組み合わせを作成して欠損日を0埋めする
        all_dates = pd.date_range(start=df_daily["date"].min(), end=df_daily["date"].max())
        all_chars = ["勇者", "戦士", "魔法使い", "僧侶"]
        mux = pd.MultiIndex.from_product([all_dates, all_chars], names=["date", "character"])

        df_full = df_daily.set_index(["date", "character"]).reindex(mux, fill_value=0).reset_index()
        df_full = df_full.sort_values(["character", "date"])

        # キャラクターごとに7日間移動平均を算出
        df_full["exp_ma"] = df_full.groupby("character")["exp"].transform(lambda x: x.rolling(window=7, min_periods=1).mean())

        # 重ね合わせグラフの作成
        chart = alt.Chart(df_full).mark_line(point=False).encode(
            x=alt.X('date:T', title='日付'),
            y=alt.Y('exp_ma:Q', title='獲得EXP (7日間移動平均)'),
            color=alt.Color('character:N', title='キャラクター', scale=alt.Scale(scheme='category10')),
            tooltip=['date', 'character', 'exp_ma']
        ).properties(height=400).interactive()

        st.altair_chart(chart, width="stretch")

    except Exception as e:
        st.error(f"グラフの描画中にエラーが発生しました: {e}")

def render_level_up(battle):
    party = battle.players
    st.header("🌙 週末イベント：成長の刻")
    log_csv = config.RPG_EX_CSV
    for i, player in enumerate(party):
        role = player.name
        if role in st.session_state.confirmed_roles:
            st.write("✅ 成長確定済み")
            continue
        gained_exp = render_review_week(role, log_csv)
        if st.button("📈 成長を確定する", key = role):
            level_ups = confirm_weekly_growth(i, gained_exp)
            level = st.session_state["battle"].players[i].level
            if level_ups > 0:
                st.balloons()
                st.success(
                    f"🎉 {role}は {level_ups} 回レベルアップ！\n"
                    f"現在 Lv {level}"
                )
            else:
                st.info("経験は積んだが、まだ次の境地には届かなかった…")
    render_exp_charts(log_csv)
