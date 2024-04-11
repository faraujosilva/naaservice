from src.device.interface import IDevice

class Device(IDevice):
    def __init__(self, name: str, ip: str, type:str, port:int, vendor: str, os: str, driver: str=None):
        self.__name = name
        self.__ip = ip
        self.__port = 22 if not port else port
        self.__type = type
        self.__vendor = vendor
        self.__os = os
        self.__driver = driver
    
    def get_driver(self):
        return self.__driver
    
    def get_ip(self):
        return self.__ip
    
    def get_os(self):
        return self.__os
    
    def get_type(self):
        return self.__type
    
    def get_vendor(self):
        return self.__vendor
    
    def get_port(self):
        return self.__port
    
    def to_dict(self):
        return {
            'name': self.__name,
            'ip': self.__ip,
            'port': self.__port,
            'type': self.__type,
            'vendor': self.__vendor,
            'os': self.__os,
            'driver': self.__driver
        }
    
    def set_driver(self, driver):
        self.__driver = driver