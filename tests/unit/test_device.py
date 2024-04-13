# from src.device.interface import IDevice


# class BaseDevice(IDevice):
#     """BaseDevice class to represent a device in the network."""
#     def __init__(
#         self,
#         name: str,
#         ip: str,
#         type: str,
#         port: int,
#         vendor: str,
#         os: str,
#         driver: str = None,
#     ):
#         self.__name = name
#         self.__ip = ip
#         self.__port = 22 if not port else port
#         self.__type = type
#         self.__vendor = vendor
#         self.__os = os
#         self.__driver = driver

#     def get_driver(self):
#         """Get the driver for the device."""
#         return self.__driver

#     def get_ip(self):
#         """Get the IP address of the device."""
#         return self.__ip

#     def get_os(self):
#         """Get the OS of the device."""
#         return self.__os

#     def get_type(self):
#         """Get the type of the device."""
#         return self.__type

#     def get_vendor(self):
#         """Get the vendor of the device."""
#         return self.__vendor

#     def get_port(self):
#         """Get the port of the device."""
#         return self.__port

#     def to_dict(self):
#         """Convert the device to a dictionary."""
#         return {
#             "name": self.__name,
#             "ip": self.__ip,
#             "port": self.__port,
#             "type": self.__type,
#             "vendor": self.__vendor,
#             "os": self.__os,
#             "driver": self.__driver,
#         }

#     def set_driver(self, driver):
#         """Set the driver for the device."""
#         self.__driver = driver

import unittest
from unittest.mock import patch, MagicMock
from src.device.base import BaseDevice

class TestBaseDevice(unittest.TestCase):
    @patch('src.device.base.IDevice')
    def test_init(self, mock_idevice):
        # Arrange
        name = 'test_name'
        ip = 'test_ip'
        type = 'test_type'
        port = 22
        vendor = 'test_vendor'
        os = 'test_os'
        driver = 'test_driver'
        # Act
        basedevice = BaseDevice(name, ip, type, port, vendor, os, driver)
        # Assert
        self.assertEqual(basedevice._BaseDevice__name, name)
        self.assertEqual(basedevice._BaseDevice__ip, ip)
        self.assertEqual(basedevice._BaseDevice__port, port)
        self.assertEqual(basedevice._BaseDevice__type, type)
        self.assertEqual(basedevice._BaseDevice__vendor, vendor)
        self.assertEqual(basedevice._BaseDevice__os, os)
        self.assertEqual(basedevice._BaseDevice__driver, driver)

    @patch('src.device.base.IDevice')
    def test_get_driver(self, mock_idevice):
        # Arrange
        name = 'test_name'
        ip = 'test_ip'
        type = 'test_type'
        port = 22
        vendor = 'test_vendor'
        os = 'test_os'
        driver = 'test_driver'
        basedevice = BaseDevice(name, ip, type, port, vendor, os, driver)
        # Act
        driver = basedevice.get_driver()
        # Assert
        self.assertEqual(driver, driver)

    @patch('src.device.base.IDevice')
    def test_get_ip(self, mock_idevice):
        # Arrange
        name = 'test_name'
        ip = 'test_ip'
        type = 'test_type'
        port = 22
        vendor = 'test_vendor'
        os = 'test_os'
        driver = 'test_driver'
        basedevice = BaseDevice(name, ip, type, port, vendor, os, driver)
        # Act
        ip = basedevice.get_ip()
        # Assert
        self.assertEqual(ip, ip)

    @patch('src.device.base.IDevice')
    def test_get_os(self, mock_idevice):
        # Arrange
        name = 'test_name'
        ip = 'test_ip'
        type = 'test_type'
        port = 22
        vendor = 'test_vendor'
        os = 'test_os'
        driver = 'test_driver'
        basedevice = BaseDevice(name, ip, type, port, vendor, os, driver)
        # Act
        os = basedevice.get_os()
        # Assert
        self.assertEqual(os, os)
        
    @patch('src.device.base.IDevice')
    def test_get_type(self, mock_idevice):
        # Arrange
        name = 'test_name'
        ip = 'test_ip'
        type = 'test_type'
        port = 22
        vendor = 'test_vendor'
        os = 'test_os'
        driver = 'test_driver'
        basedevice = BaseDevice(name, ip, type, port, vendor, os, driver)
        # Act
        type = basedevice.get_type()
        # Assert
        self.assertEqual(type, type)
        
    @patch('src.device.base.IDevice')
    def test_get_vendor(self, mock_idevice):
        # Arrange
        name = 'test_name'
        ip = 'test_ip'
        type = 'test_type'
        port = 22
        vendor = 'test_vendor'
        os = 'test_os'
        driver = 'test_driver'
        basedevice = BaseDevice(name, ip, type, port, vendor, os, driver)
        # Act
        vendor = basedevice.get_vendor()
        # Assert
        self.assertEqual(vendor, vendor)
        
    @patch('src.device.base.IDevice')
    def test_get_port(self, mock_idevice):
        # Arrange
        name = 'test_name'
        ip = 'test_ip'
        type = 'test_type'
        port = 22
        vendor = 'test_vendor'
        os = 'test_os'
        driver = 'test_driver'
        basedevice = BaseDevice(name, ip, type, port, vendor, os, driver)
        # Act
        port = basedevice.get_port()
        # Assert
        self.assertEqual(port, port)