from src.database.interface import IDatabase
from pymongo import MongoClient

class MongoDB(IDatabase):
    def __init__(self, db_name: str, collection: str, connection_string: str):
        self.db_name = db_name
        self.collection = collection
        self.connection_string = connection_string
        
    @property
    def __client(self):
        return MongoClient(self.connection_string)
    
    @property
    def __db(self):
        return self.__client[self.db_name]
    
    @property
    def __collection(self):
        return self.__db[self.collection]
    
    def get(self, query: dict=None):
        pipeline = [{"$match": query}] if query else []
        pipeline.append({"$project": {"_id": 0}})
        return self.__collection.aggregate(pipeline)    
    
    def create(self, data: dict):
        return self.__collection.insert_one(data)
    
    def update(self, query: dict, data: dict):
        return self.__collection.update_one(query, data)
    
    def delete(self, query: dict):
        return self.__collection.delete_one(query)