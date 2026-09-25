from typing import Any

from psycopg import Connection



class PostgreSQLDiagnoser:

    def __init__(self, client: Connection, database_name: str):

        self.client = client

        self.database = database_name


    def server_info(self) -> dict[str, Any]:
        query = """
            SELECT
                version() AS version,
                current_database() AS database,
                current_user AS user
        """

        with self.client.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()

            if row is None:
                return {}

            columns = [
                description.name
                for description in (cursor.description or [])
            ]

        return dict(zip(columns, row))


    def database_stats(self) -> dict[str, Any]:
        query = """
            SELECT
                datname,
                numbackends,
                xact_commit,
                xact_rollback,
                blks_read,
                blks_hit,
                tup_returned,
                tup_fetched,
                tup_inserted,
                tup_updated,
                tup_deleted,
                temp_files,
                temp_bytes,
                deadlocks,
                conflicts
            FROM pg_stat_database
            WHERE datname = current_database()
        """

        with self.client.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()

            if row is None:
                return {}

            columns = [
                description.name
                for description in (cursor.description or [])
            ]

        return dict(zip(columns, row))


    def connections(self) -> list[dict[str, Any]]:
        query = """
            SELECT
                pid,
                usename,
                datname,
                client_addr,
                client_port,
                application_name,
                state,
                wait_event_type,
                wait_event,
                backend_start,
                query_start,
                state_change,
                query
            FROM pg_stat_activity
            WHERE datname = current_database()
            ORDER BY query_start DESC NULLS LAST
        """

        with self.client.cursor() as cursor:
            cursor.execute(query)

            rows = cursor.fetchall()

            columns = [
                description.name
                for description in (cursor.description or [])
            ]

        return [
            dict(zip(columns, row))
            for row in rows
        ]


    def query_stats(self, limit: int = 20) -> list[dict[str, Any]]:
        query = """
            SELECT
                query,
                calls,
                total_exec_time,
                mean_exec_time,
                rows,
                shared_blks_hit,
                shared_blks_read,
                temp_blks_read,
                temp_blks_written
            FROM pg_stat_statements
            WHERE dbid = (
                SELECT oid
                FROM pg_database
                WHERE datname = current_database()
            )
            ORDER BY total_exec_time DESC
            LIMIT %s
        """

        with self.client.cursor() as cursor:
            cursor.execute(
                query,
                (limit,),
            )

            rows = cursor.fetchall()

            columns = [
                description.name
                for description in (cursor.description or [])
            ]

        return [
            dict(zip(columns, row))
            for row in rows
        ]


    def table_stats(self) -> list[dict[str, Any]]:
        query = """
            SELECT
                schemaname,
                relname,
                n_live_tup,
                n_dead_tup,
                seq_scan,
                seq_tup_read,
                idx_scan,
                idx_tup_fetch,
                n_tup_ins,
                n_tup_upd,
                n_tup_del,
                last_vacuum,
                last_autovacuum,
                last_analyze,
                last_autoanalyze
            FROM pg_stat_user_tables
            ORDER BY n_live_tup DESC
        """

        with self.client.cursor() as cursor:
            cursor.execute(query)

            rows = cursor.fetchall()

            columns = [
                description.name
                for description in (cursor.description or [])
            ]

        return [
            dict(zip(columns, row))
            for row in rows
        ]


    def indexes(self) -> list[dict[str, Any]]:
        query = """
            SELECT
                schemaname,
                tablename,
                indexname,
                indexdef
            FROM pg_indexes
            WHERE schemaname NOT IN (
                'pg_catalog',
                'information_schema'
            )
            ORDER BY
                schemaname,
                tablename,
                indexname
        """

        with self.client.cursor() as cursor:
            cursor.execute(query)

            rows = cursor.fetchall()

            columns = [
                description.name
                for description in (cursor.description or [])
            ]

        return [
            dict(zip(columns, row))
            for row in rows
        ]


    def index_usage(self) -> list[dict[str, Any]]:
        query = """
            SELECT
                schemaname,
                relname AS table_name,
                indexrelname AS index_name,
                idx_scan,
                idx_tup_read,
                idx_tup_fetch
            FROM pg_stat_user_indexes
            ORDER BY idx_scan ASC
        """

        with self.client.cursor() as cursor:
            cursor.execute(query)

            rows = cursor.fetchall()

            columns = [
                description.name
                for description in (cursor.description or [])
            ]

        return [
            dict(zip(columns, row))
            for row in rows
        ]


    def table_sizes(self) -> list[dict[str, Any]]:
        query = """
            SELECT
                schemaname,
                tablename,
                pg_size_pretty(
                    pg_total_relation_size(
                        schemaname || '.' || tablename
                    )
                ) AS total_size,
                pg_total_relation_size(
                    schemaname || '.' || tablename
                ) AS total_size_bytes,
                pg_size_pretty(
                    pg_relation_size(
                        schemaname || '.' || tablename
                    )
                ) AS table_size,
                pg_relation_size(
                    schemaname || '.' || tablename
                ) AS table_size_bytes,
                pg_size_pretty(
                    pg_indexes_size(
                        schemaname || '.' || tablename
                    )
                ) AS index_size,
                pg_indexes_size(
                    schemaname || '.' || tablename
                ) AS index_size_bytes
            FROM pg_tables
            WHERE schemaname NOT IN (
                'pg_catalog',
                'information_schema'
            )
            ORDER BY total_size_bytes DESC
        """

        with self.client.cursor() as cursor:
            cursor.execute(query)

            rows = cursor.fetchall()

            columns = [
                description.name
                for description in (cursor.description or [])
            ]

        return [
            dict(zip(columns, row))
            for row in rows
        ]


    def locks(self) -> list[dict[str, Any]]:
        query = """
            SELECT
                l.pid,
                l.locktype,
                l.mode,
                l.granted,
                l.relation::regclass AS relation,
                a.usename,
                a.state,
                a.wait_event_type,
                a.wait_event,
                a.query
            FROM pg_locks l
            LEFT JOIN pg_stat_activity a
                ON a.pid = l.pid
            WHERE a.datname = current_database()
            ORDER BY l.pid
        """

        with self.client.cursor() as cursor:
            cursor.execute(query)

            rows = cursor.fetchall()

            columns = [
                description.name
                for description in (cursor.description or [])
            ]

        return [
            dict(zip(columns, row))
            for row in rows
        ]


    def replication_status(self) -> list[dict[str, Any]]:
        query = """
            SELECT
                application_name,
                client_addr,
                state,
                sync_state,
                sent_lsn,
                write_lsn,
                flush_lsn,
                replay_lsn,
                write_lag,
                flush_lag,
                replay_lag
            FROM pg_stat_replication
            ORDER BY application_name
        """

        with self.client.cursor() as cursor:
            cursor.execute(query)

            rows = cursor.fetchall()

            columns = [
                description.name
                for description in (cursor.description or [])
            ]

        return [
            dict(zip(columns, row))
            for row in rows
        ]


    def replication_slots(self) -> list[dict[str, Any]]:
        query = """
            SELECT
                slot_name,
                slot_type,
                active,
                restart_lsn,
                confirmed_flush_lsn
            FROM pg_replication_slots
            ORDER BY slot_name
        """

        with self.client.cursor() as cursor:
            cursor.execute(query)

            rows = cursor.fetchall()

            columns = [
                description.name
                for description in (cursor.description or [])
            ]

        return [
            dict(zip(columns, row))
            for row in rows
        ]


    def database_connections_summary(self) -> dict[str, Any]:
        query = """
            SELECT
                count(*) AS total_connections,
                count(*) FILTER (
                    WHERE state = 'active'
                ) AS active_connections,
                count(*) FILTER (
                    WHERE state = 'idle'
                ) AS idle_connections,
                count(*) FILTER (
                    WHERE state = 'idle in transaction'
                ) AS idle_in_transaction,
                count(*) FILTER (
                    WHERE wait_event IS NOT NULL
                ) AS waiting_connections
            FROM pg_stat_activity
            WHERE datname = current_database()
        """

        with self.client.cursor() as cursor:
            cursor.execute(query)

            row = cursor.fetchone()

            if row is None:
                return {}

            columns = [
                description.name
                for description in (cursor.description or [])
            ]

        return dict(zip(columns, row))


    def explain(self, query: str) -> Any:
        explain_query = f"""
            EXPLAIN (
                FORMAT JSON,
                COSTS TRUE,
                VERBOSE TRUE,
                BUFFERS TRUE
            )
            {query}
        """

        with self.client.cursor() as cursor:
            cursor.execute(explain_query) # pyright: ignore[reportArgumentType, reportCallIssue]

            row = cursor.fetchone()

        if row is None:
            return None

        return row[0]