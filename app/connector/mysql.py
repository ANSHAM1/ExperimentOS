from typing import Any

import pymysql
from pymysql import Connection



class MySQLClient:

    def __init__(self, host: str, port: int, username: str, password: str, database: str | None):

        self.client: Connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=5,
            read_timeout=30,
            write_timeout=30,
        )

        self.database: str | None = database


    def test_connection(self) -> dict[str, Any]:

        if self.database is None:
            return {
                "connected": False,
                "message": str("No Database Specified"),
            }

        try:
            self.client.ping(reconnect=False)

            return {
                "connected": True,
                "message": "MongoDB connection successful"
            }
        
        except pymysql.MySQLError as exc:
            return {
                "connected": False,
                "message": str(exc)
            }


    def close(self) -> None:

        self.client.close()