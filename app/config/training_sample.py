
# === 1. 曜日ごとのメニュー ===
circuit = [
    {"name": "スクワット", "sets": 2, "detail": "10~15"},
    {"name": "ベンチプレス", "sets": 2, "detail": "10~15"},
]
jump = [{"name": "なわとび", "sets": 3, "detail": "150回"}]

MENU_BY_DAY = {
    "Monday": circuit,
    "Tuesday": jump,
    "Wednesday": jump,
    "Thursday": jump,
    "Friday": circuit,
    "Saturday": jump,
    "Sunday": jump,
}


EVERY_DAY_CHECKLIST = ["寝る前のストレッチ"]
