from src.device.interface import IDevice

class Device(IDevice):
    def __init__(self, name: str, ip: str, type:str, port:int, vendor: str, os: str, driver: str=None):
        self.name = name
        self.ip = ip
        self.port = 22 if not port else port
        self.type = type
        self.vendor = vendor
        self.os = os
        self.driver = driver
    
    def get_driver(self):
        return self.driver
    
    def get_ip(self):
        return self.ip
    
    def get_os(self):
        return self.os
    
    def get_type(self):
        return self.type
    
    def get_vendor(self):
        return self.vendor
    
    def get_port(self):
        return self.port
    
    def to_dict(self):
        return self.__dict__
    
    def set_driver(self, driver):
        self.driver = driver