import unittest
from ddt import ddt, data, unpack
from unittest.mock import patch, MagicMock
from src.database.mongodb import MongoDB

@ddt
class TestMongoDB(unittest.TestCase):
    @data(
        ('test_db', 'test_collection', 'test_connection_string', 'test_query', 'test_data', 'test_update'),
    )
    @unpack
    @patch('src.database.mongodb.MongoClient')
    def test_mongodb(self, db_name, collection, connection_string, query, data, update, mock_mongo_client):
        # Arrange
        mock_mongo_client.return_value = MagicMock()
        mongodb = MongoDB(db_name, collection, connection_string)

        # Act
        get_result = mongodb.get(query)
        create_result = mongodb.create(data)
        update_result = mongodb.update(query, update)
        delete_result = mongodb.delete(query)

        # Assert
        self.assertIsNotNone(mongodb)
        self.assertIsNotNone(get_result)
        self.assertIsNotNone(create_result)
        self.assertIsNotNone(update_result)
        self.assertIsNotNone(delete_result)