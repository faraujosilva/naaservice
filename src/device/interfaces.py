from abc import ABC, abstractmethod

class IDevice(ABC):
    @abstractmethod
    def get_ip(self): pass
    @abstractmethod
    def get_os(self): pass
    @abstractmethod
    def get_vendor(self): pass
    @abstractmethod
    def get_type(self): pass
    @abstractmethod
    def get_driver(self): pass 
    @abstractmethod
    def to_dict(self): pass
    @abstractmethod
    def set_driver(self, driver: str): pass
    
class IRouter(ABC):
    @abstractmethod
    def get_routes(self): pass
    
class ISwitch(ABC):
    @abstractmethod
    def get_vlans(self): pass
    

