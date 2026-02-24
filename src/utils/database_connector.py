import psycopg2
import pandas as pd
from loguru import logger


class DatabaseConnector:
    def __init__(self):
        self.conn = None

    def connect(self, host, port, dbname, user, password):
        try:
            self.conn = psycopg2.connect(
                host=host, port=port, dbname=dbname, user=user, password=password
            )
            logger.success(f"Connected to database: {dbname}")
        except psycopg2.Error as e:
            logger.error("Connection failed:", e)

    def disconnect(self):
        try:
            self.conn.close()
            self.conn = None
        except AttributeError as e:
            logger.error("Database is not connected:", e)

    def fetch_dataframe(self, query):
        return pd.read_sql(query, self.conn)
