from abc import ABC, abstractmethod
from typing import Union
from src.models.models import SSHDriver, APIDriver, SNMPDriver

class IDriver(ABC):
    @abstractmethod
    def get_driver(self, device_driver: str) -> Union[SSHDriver, APIDriver, SNMPDriver]:
        pass
    
    @abstractmethod
    def get_driver_order(self) -> list:
        pass