from abc import ABC, abstractmethod
from src.models.device_models import *

class IDevice(ABC):
    """
        Abstract class for Device that needs to implement general and common for all devices methods
    """
    @abstractmethod
    def get_ip(self) -> str:
        pass
    
    @abstractmethod
    def get_os(self) -> str:
        pass
    
    @abstractmethod
    def get_type(self) -> str:
        pass
    
    @abstractmethod
    def get_vendor(self) -> str:
        pass
    
    @abstractmethod
    def get_port(self) -> int:
        pass
    
    @abstractmethod
    def get_driver(self) -> str:
        pass
    
    @abstractmethod
    def to_dict(self) -> dict:
        pass
    
    @abstractmethod
    def set_driver(self, driver: str) -> None:
        pass
    
    @abstractmethod
    def get_interfaces(self) -> List[Interfaces]:
        pass
    
    @abstractmethod
    def get_cpu_usage(self) -> CPUUsage:
        pass

class IRouter(ABC):
    """
        Abstract class for Router that needs to implement router specific methods
    """
    @abstractmethod
    def get_routes(self) -> List[Routes]:
        pass
    
    @abstractmethod
    def get_arp_table(self) -> List[ArpTable]:
        pass