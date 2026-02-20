import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from loguru import logger

# ------------------------

load_dotenv()
DB_URL = os.getenv("DB_URL_LEGACY")
CSV_PATH = "data/raw/customer_dump.csv"

# ------------------------


def load_data() -> str | None:
    if not os.path.exists(CSV_PATH):
        return "Data does not exist."
    else:
        logger.info("Loading data...")
        df = pd.read_csv(CSV_PATH, sep=";")
        engine = create_engine(DB_URL)

    try:
        df.to_sql(
            "legacy",
            engine,
            schema="raw_data",
            if_exists="replace",
            index=False,
            chunksize=500,
        )
        logger.success("SUCCESS")

    except Exception as e:
        logger.error(f"Following error occured: {e}")


if __name__ == "__main__":
    load_data()
