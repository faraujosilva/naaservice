from src.database.interface import IDatabase
from pymongo import MongoClient


class MongoDB(IDatabase):
    """MongoDB class to interact with MongoDB database."""
    def __init__(self, db_name: str, collection: str, connection_string: str):
        self.db_name = db_name
        self.collection = collection
        self.connection_string = connection_string

    @property
    def __client(self):
        """MongoDB client property to connect to the database."""
        return MongoClient(self.connection_string)

    @property
    def __db(self):
        """MongoDB database property to connect to the database."""
        return self.__client[self.db_name]

    @property
    def __collection(self):
        """MongoDB collection property to connect to the collection."""
        return self.__db[self.collection]

    def get(self, query: dict = None):
        """Get method to retrieve data from MongoDB database."""
        pipeline = [{"$match": query}] if query else []
        pipeline.append({"$project": {"_id": 0}})
        return self.__collection.aggregate(pipeline)

    def create(self, data: dict):
        """Create method to insert data into MongoDB database."""
        return self.__collection.insert_one(data)

    def update(self, query: dict, data: dict):
        """Update method to update data in MongoDB database."""
        return self.__collection.update_one(query, data)

    def delete(self, query: dict):
        """Delete method to delete data from MongoDB database."""
        return self.__collection.delete_one(query)
