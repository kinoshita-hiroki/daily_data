
# === 1. 曜日ごとのメニュー ===
circuit = [
    {"name": "スクワット", "sets": 2, "detail": "12~15"},
    {"name": "ベンチプレス", "sets": 2, "detail": "12~15"},
    {"name": "ローイング", "sets": 2, "detail": "10~12"},
    {"name": "デットリフト", "sets": 2, "detail": "12~15"},
    {"name": "ランジ", "sets": 2, "detail": "12~15"},
    {"name": "アームカール", "sets": 2, "detail": "12~15"},
    {"name": "ダンベルカーフレイズ", "sets": 2, "detail": "12~15"},
    {"name": "ダンベル腹筋", "sets": 2, "detail": "10~15"},
    {"name": "ショルダープレス", "sets": 2, "detail": "12~15"},
    {"name": "ヒップスラスト", "sets": 2, "detail": "12~15"},
]
yoga = [
    {"name": "ダウンドッグ", "sets": 1, "detail": "5呼吸"},
    {"name": "木のポーズ", "sets": 1, "detail": "5呼吸"},
    {"name": "片足前屈", "sets": 1, "detail": "5呼吸"},
    {"name": "英雄1のポーズ", "sets": 1, "detail": "5呼吸"},
    {"name": "シャバアーサナ", "sets": 1, "detail": "5呼吸"},
]
rest = [{"name": "瞑想", "sets": 1, "detail": "5分程度"}]
jump = [{"name": "なわとび", "sets": 4, "detail": "150回"}]

MENU_BY_DAY = {
    "Monday": circuit,
    "Tuesday": rest,
    "Wednesday": jump,
    "Thursday": rest,
    "Friday": circuit,
    "Saturday": rest,
    "Sunday": yoga,
}


EVERY_DAY_CHECKLIST = ["食べすぎない 朝", "食べすぎない 昼", "食べすぎない 夜", "風呂掃除先にやる", "寝る前ケア"]