# tests/test_utils.py
import pandas as pd

from app.utils import append_or_update


def test_append_or_update_update():
    print("test_append_or_update_update")

    df = pd.DataFrame([{"date": "2025-12-02", "minutes": 10}])
    day = "2025-12-02"
    columns= "minutes"
    value = 20

    result = append_or_update(df, day, columns, value)
    assert result.loc[0, columns] == 20

def test_append_or_update_append():
    df = pd.DataFrame([{"date": "2025-12-01", "minutes": 10}])
    day = "2025-12-02"
    columns= "minutes"
    value = 20

    result = append_or_update(df, day, columns, value)
    assert len(result) == 2
