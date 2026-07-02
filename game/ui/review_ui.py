
# pyrefly: ignore [missing-import]
import altair as alt
import pandas as pd

# pyrefly: ignore [missing-import]
import streamlit as st

import app.config.config as config
from game.growth import confirm_weekly_growth


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
