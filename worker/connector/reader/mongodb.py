from typing import Any

from pymongo import MongoClient


class MongoReader:

    def __init__(self, client: MongoClient[dict[str, Any]], database_name: str):

        self.client = client

        self.database = database_name


    def collections(self):

        return self.client[self.database].list_collection_names()


    def documents(
            self, collection_name: str, filter_query: dict[str, Any] | None = None, 
            projection: dict[str, Any] | None = None, limit: int = 100
    ) -> list[dict[str, Any]]:
        
        collection = self.client[self.database][collection_name]

        return list(collection.find(filter_query or {}, projection, limit=limit))