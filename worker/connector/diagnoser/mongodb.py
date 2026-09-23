from typing import Any

from pymongo import MongoClient


class MongoDiagnostics:

    def __init__(self, client: MongoClient[dict[str, Any]]):

        self.client = client


    def server_status(self):

        return self.client.admin.command("serverStatus")


    def database_stats(self, database_name: str):

        return self.client[database_name].command("dbStats")


    def collection_stats(self, database_name: str, collection_name: str):

        return self.client[database_name].command("collStats", collection_name)
    

    def indexes(self, database_name: str, collection_name: str):

        collection = self.client[database_name][collection_name]

        return list(collection.list_indexes())


    def index_stats(self, database_name: str, collection_name: str):

        collection = self.client[database_name][collection_name]

        return list(collection.aggregate([{"$indexStats": {}}]))


    def current_operations(self):

        return self.client.admin.command("currentOp")