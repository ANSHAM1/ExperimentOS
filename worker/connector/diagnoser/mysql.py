from typing import Any

from pymysql import Connection



class MySQLDiagnostics:

    def __init__(self, client: Connection):

        self.client = client


    def server_info(self) -> dict[str, Any]:
        query = """
        SELECT
            VERSION() AS version,
            @@hostname AS hostname,
            @@port AS port,
            @@version_comment AS version_comment
        """

        with self.client.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()
            if row is None:
                return {}
            return {
                key.decode() if isinstance(key, bytes) else key:
                value.decode() if isinstance(value, bytes) else value
                for key, value in row
            }


    def performance_metrics(self) -> dict[str, Any]:
        query = """
        SHOW GLOBAL STATUS
        WHERE Variable_name IN (
            'Threads_connected',
            'Threads_running',
            'Connections',
            'Questions',
            'Queries',
            'Slow_queries',
            'Created_tmp_tables',
            'Created_tmp_disk_tables',
            'Table_locks_waited',
            'Table_locks_immediate',
            'Innodb_buffer_pool_read_requests',
            'Innodb_buffer_pool_reads',
            'Innodb_rows_read',
            'Innodb_rows_inserted',
            'Innodb_rows_updated',
            'Innodb_rows_deleted'
        )
        """

        with self.client.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        return {
            row[0]: row[1]
            for row in rows
        }


    def table_statistics(self) -> list[dict[str, Any]]:
        query = """
        SELECT
            TABLE_NAME,
            TABLE_ROWS,
            DATA_LENGTH,
            INDEX_LENGTH,
            DATA_FREE,
            CREATE_TIME,
            UPDATE_TIME
        FROM information_schema.TABLES
        WHERE TABLE_SCHEMA = DATABASE()
        ORDER BY DATA_LENGTH DESC
        """

        with self.client.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in rows]


    def indexes(self, table_name: str) -> list[dict[str, Any]]:
        query = """
        SELECT
            TABLE_NAME,
            INDEX_NAME,
            COLUMN_NAME,
            SEQ_IN_INDEX,
            NON_UNIQUE,
            CARDINALITY,
            INDEX_TYPE
        FROM information_schema.STATISTICS
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = %s
        ORDER BY INDEX_NAME, SEQ_IN_INDEX
        """

        with self.client.cursor() as cursor:
            cursor.execute(
                query,
                (table_name,),
            )

            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in rows]


    def running_queries(self) -> list[dict[str, Any]]:
        with self.client.cursor() as cursor:
            cursor.execute(
                "SHOW FULL PROCESSLIST"
            )

            rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "user": row[1],
                "host": row[2],
                "database": row[3],
                "command": row[4],
                "time": row[5],
                "state": row[6],
                "query": row[7],
            }
            for row in rows
            if row[4] != "Sleep"
        ]


    def top_queries(self, limit: int = 20) -> list[dict[str, Any]]:
        query = """
        SELECT
            DIGEST_TEXT,
            COUNT_STAR AS execution_count,
            ROUND(
                AVG_TIMER_WAIT / 1000000000,
                2
            ) AS avg_latency_ms,
            ROUND(
                SUM_TIMER_WAIT / 1000000000,
                2
            ) AS total_latency_ms,
            SUM_ROWS_EXAMINED AS rows_examined,
            SUM_ROWS_SENT AS rows_sent
        FROM performance_schema
            .events_statements_summary_by_digest
        WHERE DIGEST_TEXT IS NOT NULL
        ORDER BY SUM_TIMER_WAIT DESC
        LIMIT %s
        """

        with self.client.cursor() as cursor:
            cursor.execute(query, (limit,))

            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in rows]


    def explain(self, query: str, params: tuple[Any, ...] | None = None):
        with self.client.cursor() as cursor:
            cursor.execute(
                f"EXPLAIN {query}",
                params,
            )

            return list(cursor.fetchall())


    def locks(self) -> list[tuple[Any, ...]]:
        query = """
        SELECT
            OBJECT_SCHEMA,
            OBJECT_NAME,
            INDEX_NAME,
            LOCK_TYPE,
            LOCK_MODE,
            LOCK_STATUS,
            LOCK_DATA
        FROM performance_schema.data_locks
        """

        with self.client.cursor() as cursor:
            cursor.execute(query)

            return list(cursor.fetchall())


    def lock_waits(self) -> list[dict[str, Any]]:
        query = """
        SELECT *
        FROM performance_schema.data_lock_waits
        """

        with self.client.cursor() as cursor:
            cursor.execute(query)

            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in rows]