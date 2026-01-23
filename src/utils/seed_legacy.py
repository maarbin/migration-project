import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DB_URL_LEGACY")
CSV_PATH = "data/raw/customers_dump.csv"


def load_data():
    if not os.path.exists(CSV_PATH):
        return "Data does not exist."
    else:
        print("Loading data...")
        df = pd.read_csv(CSV_PATH)
        engine = create_engine(DB_URL)

    try:
        df.to_sql(
            "legacy",
            engine,
            schema="raw_data",
            if_exists="append",
            index=False,
            chunksize=100,
        )
        print("SUCCESS")

    except Exception as e:
        print(f"Following error occured: {e}")


if __name__ == "__main__":
    load_data()
