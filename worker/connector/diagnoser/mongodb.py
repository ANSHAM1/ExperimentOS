from typing import Any

from pymongo import MongoClient


class MongoDiagnostics:

    def __init__(self, client: MongoClient[dict[str, Any]], database_name: str):

        self.client = client

        self.database = database_name


    def server_status(self):

        return self.client.admin.command("serverStatus")


    def database_stats(self):

        return self.client[self.database].command("dbStats")


    def collection_stats(self, collection_name: str):

        return self.client[self.database].command("collStats", collection_name)
    

    def indexes(self, collection_name: str):

        collection = self.client[self.database][collection_name]

        return list(collection.list_indexes())


    def index_stats(self, collection_name: str):

        collection = self.client[self.database][collection_name]

        return list(collection.aggregate([{"$indexStats": {}}]))


    def current_operations(self):

        return self.client.admin.command("currentOp")