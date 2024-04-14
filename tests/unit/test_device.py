import unittest
from unittest.mock import MagicMock, patch
from src.database.mongodb import MongoDB
from ddt import ddt, data, unpack
from src.device.interfaces import IDevice, IRouter, ISwitch
from src.connector.conector_factory import ConnectorFactory
from src.device.device_factory import DeviceFactory

@ddt
class TestDevice(unittest.TestCase):
    @data(
        ('1.2.3.4', 'router', 'ios', 'ssh', 22, 'SSH IOS: show ip route', 'IOS Base'),
        ('1.2.3.4', 'router', 'nxos', 'ssh', 22, 'SSH NXOS: show ip route vrf all', 'NXOS Base'),
        ('1.2.3.4', 'switch', 'ios', 'ssh', 22, 'SSH IOS: show vlan br', 'IOS Base'),
        ('1.2.3.4', 'switch', 'nxos', 'ssh', 22, 'SSH NXOS: show vlan all', 'NXOS Base'),
        ('1.2.3.4', 'sdwan', 'viptela', 'api', 443, 'API: /routes/all_vrfs', 'API Base'),
        ('1.2.3.4', 'sdwan', 'viptela', 'api', None, 'API: /routes/all_vrfs', 'API Base'),
        ('1.2.3.4', 'router', 'ios', None, 22, 'SSH IOS: show ip route', 'IOS Base'),
    )
    @patch('src.database.mongodb.MongoDB.get')
    @patch('src.database.mongodb.MongoClient')
    @unpack
    def test_devices(self, ip: str, d_type: str, os: str, driver: str, port: int, expected1, expected2, mock_mongo_client, mock_mongo_get):
        # Arrange
        db_name = 'test_db'
        collection = 'test_collection'
        connection_string = 'test_connection_string'
        expected_device_data = {'vendor': 'cisco', 'type': d_type, 'os': os, 'ip': ip, 'driver': driver, 'name': 'R1', 'port': port}
        
        mock_mongo_client.return_value = MagicMock()
        mongodb = MongoDB(db_name, collection, connection_string)
        mock_mongo_get.return_value = [expected_device_data]
        
        device_factory = DeviceFactory()
        connector_factory = ConnectorFactory()
        connector = connector_factory.create_connector('netmiko')
        
        # Act
        devices = device_factory.create_device(ip, mongodb, connector)
        
        # Assert
        self.assertEqual(len(devices), 1)  # Assuming that one device is expected to be created
        self.assertIsInstance(devices[0], IDevice)  # Assuming that the device should be an IRouter
        self.assertEqual(devices[0].get_ip(), ip)
        mock_mongo_get.assert_called_with({'ip': ip})
        if isinstance(devices[0], IRouter):
            self.assertEqual(devices[0].get_routes(), expected1)
        elif isinstance(devices[0], ISwitch):
            self.assertEqual(devices[0].get_vlans(), expected1)
            
        self.assertEqual(devices[0].get_os(), os)
        self.assertEqual(devices[0].BASE, expected2)