import psycopg2
import pandas as pd
from loguru import logger


class DatabaseConnector:
    def __init__(self):
        self.conn = None

    def connect(
        self, host: str, port: int, dbname: str, user: str, password: str
    ) -> None:
        """
        Establishes a connection to the PostgreSQL database.

        Raises:
            RuntimeError: Connection fails.
        """
        try:
            self.conn = psycopg2.connect(
                host=host, port=port, dbname=dbname, user=user, password=password
            )
            logger.success(f"Connected to database: {dbname}")
        except psycopg2.Error:
            logger.error("Connection failed")

    def disconnect(self) -> None:
        """
        Disconnect from the PostgreSQL database.

        Raises:
            AttributeError: Function call without established connection.
        """
        try:
            self.conn.close()
            self.conn = None
        except AttributeError:
            logger.error("Database is not connected")

    def fetch_dataframe(self, query: str) -> pd.DataFrame:
        """Fetch SQL query result into DataFrame

        Args:
            query (str): SQL query

        Raises:
            RuntimeError: Invalid query

        Returns:
            pd.DataFrame: Result of the query
        """
        try:
            return pd.read_sql(query, self.conn)
        except psycopg2.Error as e:
            logger.error("Database query failed")
            raise RuntimeError("Database fetch failed") from e
