import unittest
from unittest.mock import patch, MagicMock

from src.database.interface import IDatabase
from src.database.mongodb import MongoDB

class TestMongoDB(unittest.TestCase):
    @patch('src.database.mongodb.MongoClient')
    def test_init(self, mock_mongo_client):
        # Arrange
        db_name = 'test_db'
        collection = 'test_collection'
        connection_string = 'test_connection_string'
        # Act
        mongodb = MongoDB(db_name, collection, connection_string)
        # Assert
        self.assertEqual(mongodb.db_name, db_name)
        self.assertEqual(mongodb.collection, collection)
        self.assertEqual(mongodb.connection_string, connection_string)

    @patch('src.database.mongodb.MongoClient')
    def test_client(self, mock_mongo_client):
        # Arrange
        db_name = 'test_db'
        collection = 'test_collection'
        connection_string = 'test_connection_string'
        mongodb = MongoDB(db_name, collection, connection_string)
        # Act
        client = mongodb._MongoDB__client
        # Assert
        mock_mongo_client.assert_called_with(connection_string)
        self.assertEqual(client, mock_mongo_client.return_value)

    @patch('src.database.mongodb.MongoClient')
    def test_db(self, mock_mongo_client):
        # Arrange
        db_name = 'test_db'
        collection = 'test_collection'
        connection_string = 'test_connection_string'
        mongodb = MongoDB(db_name, collection, connection_string)
        # Act
        db = mongodb._MongoDB__db
        # Assert
        mock_mongo_client.assert_called_with(connection_string)
        self.assertEqual(db, mock_mongo_client.return_value[db_name])

    @patch('src.database.mongodb.MongoClient')
    def test_collection(self, mock_mongo_client):
        # Arrange
        db_name = 'test_db'
        collection = 'test_collection'
        connection_string = 'test_connection_string'
        mongodb = MongoDB(db_name, collection, connection_string)
        # Act
        collection = mongodb._MongoDB__collection
        # Assert
        mock_mongo_client.assert_called_with(connection_string)
        self.assertEqual(collection, mock_mongo_client.return_value[db_name][collection])

    @patch('src.database.mongodb.MongoClient')
    def test_get(self, mock_mongo_client):
        # Arrange
        db_name = 'test_db'
        collection = 'test_collection'
        connection_string = 'test_connection_string'
        mongodb = MongoDB(db_name, collection, connection_string)
        query = {'test_key': 'test_value'}
        pipeline = [{"$match": query}, {"$project": {"_id": 0}}]
        
        mongodb._MongoDB__collection.aggregate = MagicMock()
        
        # Act
        result = mongodb.get(query)
        # Assert
        mongodb._MongoDB__collection.aggregate.assert_called_with(pipeline)
        
    @patch('src.database.mongodb.MongoClient')
    def test_create(self, mock_mongo_client):
        # Arrange
        db_name = 'test_db'
        collection = 'test_collection'
        connection_string = 'test_connection_string'
        mongodb = MongoDB(db_name, collection, connection_string)
        data = {'test_key': 'test_value'}
        
        mongodb._MongoDB__collection.insert_one = MagicMock()
        
        # Act
        result = mongodb.create(data)
        # Assert
        mongodb._MongoDB__collection.insert_one.assert_called_with(data)

        self.assertEqual(result, mongodb._MongoDB__collection.insert_one.return_value)
    
    @patch('src.database.mongodb.MongoClient')
    def test_update(self, mock_mongo_client):
        # Arrange
        db_name = 'test_db'
        collection = 'test_collection'
        connection_string = 'test_connection_string'
        mongodb = MongoDB(db_name, collection, connection_string)
        query = {'test_key': 'test_value'}
        data = {'$set': {'test_key': 'test_value'}}
        
        mongodb._MongoDB__collection.update_one = MagicMock()
        
        # Act
        result = mongodb.update(query, data)
        # Assert
        mongodb._MongoDB__collection.update_one.assert_called_with(query, data)

        self.assertEqual(result, mongodb._MongoDB__collection.update_one.return_value)
    
    @patch('src.database.mongodb.MongoClient')
    def test_delete(self, mock_mongo_client):
        # Arrange
        db_name = 'test_db'
        collection = 'test_collection'
        connection_string = 'test_connection_string'
        mongodb = MongoDB(db_name, collection, connection_string)
        query = {'test_key': 'test_value'}
        
        mongodb._MongoDB__collection.delete_one = MagicMock()
        
        # Act
        result = mongodb.delete(query)
        # Assert
        mongodb._MongoDB__collection.delete_one.assert_called_with(query)

        self.assertEqual(result, mongodb._MongoDB__collection.delete_one.return_value)
    