from typing import Any

import psycopg
from psycopg import Connection



class PostgreSQLConnection:

    def __init__(self, host: str, port: int, username: str, password: str, database: str | None):

        self.client: Connection = psycopg.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            dbname=database,
            connect_timeout=5,
        )

        self.database: str | None = database


    def test_connection(self) -> dict[str, Any]:

        if self.database is None:
            return {
                "connected": False,
                "message": str("No Database Specified")
            }

        try:
            result = self.client.execute("SELECT 1").fetchone()

            return {
                "connected": result is not None and result[0] == 1,
                "message": "MongoDB connection successful"
            }

        except psycopg.Error as exc:
            return {
                "connected": False,
                "message": str(exc)
            }


    def close(self) -> None:
        
        self.client.close()