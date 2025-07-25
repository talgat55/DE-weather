import requests
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine

url = "https://api.open-meteo.com/v1/forecast"
def run_main():
    params = {
        "latitude": 52.52,
        "longitude": 13.41,
        "hourly": "temperature_2m"
    }

    response = requests.get(url, params)
    data = response.json()

    timestamps = data["hourly"]["time"]
    temperature = data["hourly"]["temperature_2m"]

    df = pd.DataFrame({
        "timestamp": pd.to_datetime(timestamps),
        "temperature": temperature,
        "extracted_at": datetime.now().date(),
    })

    engine = create_engine("postgresql+psycopg2://de_user:de_pass@postgres:5432/de_weather")

    df.to_sql("weather_berlin", engine, if_exists="append", index=False)

    print(f" {df}")
