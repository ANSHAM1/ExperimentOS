from typing import Any

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError


class MongoDBClient:

    def __init__(self, uri: str):

        self.client: MongoClient[dict[str, Any]] = MongoClient(uri, serverSelectionTimeoutMS=5000)


    def test_connection(self) -> dict[str, Any]:

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


    def list_databases(self) -> list[str]:

        return self.client.list_database_names()
    

    def close(self):
        
        self.client.close()