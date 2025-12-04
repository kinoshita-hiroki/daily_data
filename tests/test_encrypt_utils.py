import os
import tempfile
import pandas as pd
import pytest
from cryptography.fernet import Fernet, InvalidToken

from crypt.encrypt_utils import (
    get_fernet_from_env,
    save_encrypted_csv,
    load_encrypted_csv,
)

# ---------- get_fernet_from_env ----------
def test_get_fernet_from_env_success(monkeypatch):
    key = Fernet.generate_key().decode()
    monkeypatch.setenv("FERNET_KEY", key)

    f = get_fernet_from_env("FERNET_KEY")
    assert isinstance(f, Fernet)


def test_get_fernet_from_env_none(monkeypatch):
    monkeypatch.delenv("FERNET_KEY", raising=False)

    f = get_fernet_from_env("FERNET_KEY")
    assert f is None


# ---------- save_encrypted_csv / load_encrypted_csv ----------
def test_save_and_load_encrypted_csv():
    fernet = Fernet(Fernet.generate_key())
    df_original = pd.DataFrame({"name": ["A", "B"], "value": [1, 2]})

    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "test.csv.enc")

        # Save encrypted
        save_encrypted_csv(path, df_original, fernet)
        assert os.path.exists(path)

        # Load encrypted
        df_loaded = load_encrypted_csv(path, fernet)

        pd.testing.assert_frame_equal(df_original, df_loaded)


def test_load_encrypted_csv_file_not_exist():
    fernet = Fernet(Fernet.generate_key())

    # ファイル無し → 空の DataFrame
    empty_df = load_encrypted_csv("no_such_file.csv", fernet, columns=["a", "b"])

    assert isinstance(empty_df, pd.DataFrame)
    assert list(empty_df.columns) == ["a", "b"]
    assert empty_df.empty


def test_load_encrypted_csv_invalid_key():
    fernet1 = Fernet(Fernet.generate_key())
    fernet2 = Fernet(Fernet.generate_key())  # 違うキー

    df = pd.DataFrame({"x": [1, 2]})

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        path = tmp.name

    # 保存
    save_encrypted_csv(path, df, fernet1)

    # 誤ったキーでロード → ValueError
    with pytest.raises(ValueError):
        load_encrypted_csv(path, fernet2)

    os.remove(path)
