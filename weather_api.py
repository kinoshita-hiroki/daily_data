# --------------------------
# Weather API
# --------------------------
from datetime import date, datetime, timedelta
def fetch_current_weather(city: str, api_key: str):
    if not api_key:
        return None
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ja"
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        d = r.json()
        return {"desc": d["weather"][0]["description"], "temp": d["main"]["temp"], "icon": d["weather"][0]["icon"]}
    except Exception:
        return None

def fetch_forecast_noon(city: str, api_key: str):
    if not api_key:
        return {}
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=ja"
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()
        forecasts = {}
        for entry in data.get("list", []):
            dt = datetime.fromtimestamp(entry["dt"])
            if dt.hour == 12:
                forecasts[dt.date().isoformat()] = {
                    "desc": entry["weather"][0]["description"],
                    "temp": entry["main"]["temp"],
                    "icon": entry["weather"][0]["icon"]
                }
        return forecasts
    except Exception:
        return {}