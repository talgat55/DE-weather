from sqlalchemy import create_engine

def load_to_db(df):
    engine = create_engine("postgresql+psycopg2://de_user:de_pass@postgres:5432/de_weather")
    df.to_sql("weather_data", engine, if_exists="append", index=False)