from typing import Any

import sqlglot
from sqlglot import exp
from pymysql import Connection


class MySQLReader:

    def __init__(self, client: Connection, database_name: str):

        self.client = client

        self.database = database_name


    def tables(self) -> list[str]:

        with self.client.cursor() as cursor:
            cursor.execute(
                """
                SELECT TABLE_NAME
                FROM information_schema.TABLES
                WHERE TABLE_SCHEMA = %s
                """,
                (self.database,),
            )

            rows = cursor.fetchall()

        return [
            row[0]
            for row in rows
        ]


    def datarows(self, query: str) -> list[dict[str, Any]]:

        self._validate_read_query(query)

        with self.client.cursor() as cursor:
            cursor.execute(query)

            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]

            return [
                dict(zip(columns, row))
                for row in rows
            ]


    @staticmethod
    def _validate_read_query(query: str) -> None:

        statements = sqlglot.parse(
            query,
            dialect="mysql",
        )

        if len(statements) != 1:
            raise ValueError(
                "Only one SQL statement is allowed."
            )

        statement = statements[0]

        if not isinstance(statement, exp.Select):
            raise ValueError(
                "Only SELECT queries are allowed."
            )