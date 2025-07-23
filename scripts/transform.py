import pandas as pd

def transform_data(file_path):
    df = pd.read_csv(file_path)
    df["temp_C"] = df["temperature_2m"]
    df["humidity_percent"] = df["relative_humidity_2m"]
    return df[["temp_C", "humidity_percent"]]
