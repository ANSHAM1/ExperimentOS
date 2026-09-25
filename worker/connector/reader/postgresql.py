from typing import Any

import sqlglot
from sqlglot import exp
from psycopg import Connection



class PostgreSQLReader:

    def __init__(self, client: Connection, database_name: str):

        self.client = client

        self.database = database_name


    def tables(self) -> list[str]:

        query = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """

        with self.client.cursor() as cursor:
            cursor.execute(query)

            rows = cursor.fetchall()

        return [
            row[0]
            for row in rows
        ]


    def datarows(self, query: str) -> list[dict[str, Any]]:

        self._validate_read_query(query)

        with self.client.cursor() as cursor:
            cursor.execute(query)  # pyright: ignore[reportArgumentType, reportCallIssue]

            if cursor.description is None:
                return []

            columns = [
                description.name
                for description in cursor.description
            ]

            rows = cursor.fetchall()

        return [
            dict(zip(columns, row))
            for row in rows
        ]


    @staticmethod
    def _validate_read_query(query: str) -> None:

        statements = sqlglot.parse(
            query,
            dialect="postgres",
        )

        if len(statements) != 1:
            raise ValueError(
                "Only one SQL statement is allowed."
            )

        if not isinstance(statements[0], exp.Select):
            raise ValueError(
                "Only SELECT queries are allowed."
            )