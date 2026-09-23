from typing import Any

from pymongo import MongoClient


class MongoReader:

    def __init__(self, client: MongoClient[dict[str, Any]]):

        self.client = client


    def collections(self, database_name: str):

        return self.client[database_name].list_collection_names()


    def documents(
            self, database_name: str, collection_name: str, filter_query: dict[str, Any] | None = None, 
            projection: dict[str, Any] | None = None, limit: int = 100
    ) -> list[dict[str, Any]]:
        
        collection = self.client[database_name][collection_name]

        return list(collection.find(filter_query or {}, projection, limit=limit))