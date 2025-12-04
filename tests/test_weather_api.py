import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
import requests

from app.weather_api import (
    fetch_current_weather,
    fetch_forecast_noon,
)

# your_module_name はファイル名（例：weather_api）に変更してください

# --------------------------
# fetch_current_weather
# --------------------------

def test_fetch_current_weather_no_api_key():
    assert fetch_current_weather("Tokyo", "") is None


def test_fetch_current_weather_success():
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "weather": [{"description": "clear", "icon": "01d"}],
        "main": {"temp": 22.5},
    }

    with patch("app.weather_api.requests.get", return_value=mock_response):
        result = fetch_current_weather("Tokyo", "dummy_key")

    assert result == {"desc": "clear", "temp": 22.5, "icon": "01d"}


def test_fetch_current_weather_exception():
    with patch("app.weather_api.requests.get", side_effect=Exception("Error")):
        result = fetch_current_weather("Tokyo", "dummy_key")

    assert result is None


# --------------------------
# fetch_forecast_noon
# --------------------------

def test_fetch_forecast_noon_no_api_key():
    assert fetch_forecast_noon("Tokyo", "") == {}


def test_fetch_forecast_noon_success():
    # 12:00 の UNIX タイムスタンプを作成
    dt = datetime(2025, 1, 1, 12, 0)
    ts = int(dt.timestamp())

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "list": [
            {
                "dt": ts,
                "weather": [{"description": "rain", "icon": "10d"}],
                "main": {"temp": 18.3},
            },
            {
                # 15:00 のためスキップされる
                "dt": int(datetime(2025, 1, 1, 15, 0).timestamp()),
                "weather": [{"description": "cloudy", "icon": "02d"}],
                "main": {"temp": 20.1},
            },
        ]
    }

    with patch("app.weather_api.requests.get", return_value=mock_response):
        result = fetch_forecast_noon("Tokyo", "dummy_key")

    # 12時だけ含まれる
    assert result == {
        "2025-01-01": {"desc": "rain", "temp": 18.3, "icon": "10d"}
    }


def test_fetch_forecast_noon_exception():
    with patch("app.weather_api.requests.get", side_effect=Exception("Error")):
        result = fetch_forecast_noon("Tokyo", "dummy_key")

    assert result == {}
