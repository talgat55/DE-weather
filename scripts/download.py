import pandas as pd
import requests
import os

def download_weather_date():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 52.52,
        "longitude": 13.41,
        "hourly": "temperature_2m,relative_humidity_2m",
        "timezone": "auto"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        hourly_data = data["hourly"]
        df = pd.DataFrame(hourly_data)

        file_path = f"./tmp/weather_{pd.Timestamp.now().date()}.csv"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_csv(file_path, index=False)

        print(f"✅ Сохранено: {file_path}")
        return file_path
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при подключении к API: {e}")
        return None

