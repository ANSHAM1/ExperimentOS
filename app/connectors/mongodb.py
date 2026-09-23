from typing import Any

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from urllib.parse import urlparse, unquote


class MongoDBClient:

    @staticmethod
    def get_database_name(uri: str) -> str | None:

        parsed = urlparse(uri)

        if parsed.scheme not in {"mongodb", "mongodb+srv"}:
            return None

        database = parsed.path.lstrip("/")

        if not database:
            return None

        return unquote(database)


    def __init__(self, uri: str):

        self.client: MongoClient[dict[str, Any]] = MongoClient(uri, serverSelectionTimeoutMS=5000)

        self.database = self.get_database_name(uri)


    def test_connection(self) -> dict[str, Any]:

        if self.database is None:
            return {
                "connected": False,
                "message": str("No Database Specified"),
            }

        try:
            result = self.client.admin.command("ping")

            return {
                "connected": result.get("ok") == 1,
                "message": "MongoDB connection successful",
            }

        except (ConnectionFailure, ServerSelectionTimeoutError) as exc:
            return {
                "connected": False,
                "message": str(exc),
            }


    def ping(self):

        return self.client.admin.command("ping")
    

    def close(self):

        self.client.close()