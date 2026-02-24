import os
from dotenv import load_dotenv
from loguru import logger
from utils.database_connector import DatabaseConnector

# ------------------------

load_dotenv()
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOST = os.getenv("POSTGRES_HOST")
PORT = os.getenv("POSTGRES_PORT")
DBNAME = "legacy_db"
OUTPUT_PATH = "data/legacy_dump/legacy_dump.csv"

# ------------------------


def extract():
    connector = DatabaseConnector()

    try:
        connector.connect(
            host=HOST, port=PORT, dbname=DBNAME, user=USER, password=PASSWORD
        )
        df = connector.fetch_dataframe(query="SELECT * FROM raw_data.legacy")
        df.to_csv(OUTPUT_PATH, index=False)
        logger.success(f"Database dump saved to {OUTPUT_PATH}")
        return OUTPUT_PATH
    except RuntimeError:
        logger.error("Pipeline aborted - database operation failed.")
    except OSError:
        logger.error("Export failed - directory does not exist.")
    finally:
        connector.disconnect()


# ------------------------

if __name__ == "__main__":
    extract()
