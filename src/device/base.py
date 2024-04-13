from src.device.interface import IDevice


class BaseDevice(IDevice):
    """BaseDevice class to represent a device in the network."""
    def __init__(
        self,
        name: str,
        ip: str,
        type: str,
        port: int,
        vendor: str,
        os: str,
        driver: str = None,
    ):
        self.__name = name
        self.__ip = ip
        self.__port = 22 if not port else port
        self.__type = type
        self.__vendor = vendor
        self.__os = os
        self.__driver = driver

    def get_driver(self):
        """Get the driver for the device."""
        return self.__driver

    def get_ip(self):
        """Get the IP address of the device."""
        return self.__ip

    def get_os(self):
        """Get the OS of the device."""
        return self.__os

    def get_type(self):
        """Get the type of the device."""
        return self.__type

    def get_vendor(self):
        """Get the vendor of the device."""
        return self.__vendor

    def get_port(self):
        """Get the port of the device."""
        return self.__port

    def to_dict(self):
        """Convert the device to a dictionary."""
        return {
            "name": self.__name,
            "ip": self.__ip,
            "port": self.__port,
            "type": self.__type,
            "vendor": self.__vendor,
            "os": self.__os,
            "driver": self.__driver,
        }

    def set_driver(self, driver):
        """Set the driver for the device."""
        self.__driver = driver
