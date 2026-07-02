import json
import sqlite3
from pprint import pprint

conn = sqlite3.connect("data/task_rpg.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS task_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    task_name TEXT,
    done INTEGER
)
""")

conn.commit()

print("テーブル作成完了")
cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
""")

print(cursor.fetchall())

conn.commit()

cursor.execute("""
SELECT *
FROM task_logs
""")

print(cursor.fetchall())



with open("logs/daily_data.json", encoding="utf-8") as f:
    data = json.load(f)

print(type(data))



first_day = next(iter(data))
pprint(data[first_day])

for date, day_data in data.items():

    for task in day_data["tasks"]:

        cursor.execute(
            """
            INSERT INTO task_logs
            (date, task_name, done)
            VALUES (?, ?, ?)
            """,
            (
                date,
                task["name"],
                int(task["done"])
            )
        )

conn.commit()

cursor.execute("""
SELECT COUNT(*)
FROM task_logs
""")

print(cursor.fetchone())
