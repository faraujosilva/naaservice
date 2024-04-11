from abc import ABC, abstractmethod

class IDevice(ABC):
    @abstractmethod
    def get_driver(self):
        pass
    
    @abstractmethod
    def get_ip(self):
        pass
    
    @abstractmethod
    def get_os(self):
        pass
    
    @abstractmethod
    def get_type(self):
        pass
    
    @abstractmethod
    def get_vendor(self):
        pass
    
    @abstractmethod
    def get_port(self):
        pass
    
    @abstractmethod
    def to_dict(self):
        pass
    
    @abstractmethod
    def set_driver(self, driver):
        pass