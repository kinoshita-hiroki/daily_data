import pandas as pd

from app.ui import update_diary_dataframe


def test_update_diary_dataframe_new_entry():
    # 空のDataFrameから開始
    df = pd.DataFrame(columns=["日付", "事実", "気持ち"])

    # 新規追加
    df = update_diary_dataframe(df, "2026-06-21", "プログラミングをした", "楽しかった")

    assert len(df) == 1
    assert df.iloc[0]["日付"] == "2026-06-21"
    assert df.iloc[0]["事実"] == "プログラミングをした"
    assert df.iloc[0]["気持ち"] == "楽しかった"


def test_update_diary_dataframe_overwrite():
    # 既存データあり
    df = pd.DataFrame(
        [["2026-06-21", "プログラミングをした", "楽しかった"]],
        columns=["日付", "事実", "気持ち"]
    )

    # 同じ日の上書き
    df = update_diary_dataframe(df, "2026-06-21", "買い物に行った", "疲れた")

    assert len(df) == 1
    assert df.iloc[0]["日付"] == "2026-06-21"
    assert df.iloc[0]["事実"] == "買い物に行った"
    assert df.iloc[0]["気持ち"] == "疲れた"


def test_update_diary_dataframe_multiple_days():
    # 既存データあり
    df = pd.DataFrame(
        [["2026-06-21", "プログラミングをした", "楽しかった"]],
        columns=["日付", "事実", "気持ち"]
    )

    # 異なる日付の追加
    df = update_diary_dataframe(df, "2026-06-22", "読書をした", "面白かった")

    assert len(df) == 2
    assert df.iloc[0]["日付"] == "2026-06-21"
    assert df.iloc[1]["日付"] == "2026-06-22"
    assert df.iloc[1]["事実"] == "読書をした"
    assert df.iloc[1]["気持ち"] == "面白かった"
