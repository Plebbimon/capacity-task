import pandas as pd
from sqlalchemy import create_engine

CSV_PATH = "data/sailing_level_raw.csv"
DB_PATH = "app/data.db"
TABLE_NAME = "sailings"

engine = create_engine(f"sqlite:///{DB_PATH}")

df = pd.read_csv(CSV_PATH)

df["ORIGIN_AT_UTC"] = pd.to_datetime(df["ORIGIN_AT_UTC"])

df.to_sql(TABLE_NAME, con=engine, if_exists="replace", index=False)

print(f"Data loaded into {DB_PATH} in table {TABLE_NAME} - Let's go sailing!")
