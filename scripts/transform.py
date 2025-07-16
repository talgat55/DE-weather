import pandas as pd

def transform_data(file_path):
    df = pd.read_csv(file_path)
    df["temp_C"] = df["temp"]
    df["humidity_percent"] = df["humidity"]
    return df[["temp_C", "humidity_percent"]]
