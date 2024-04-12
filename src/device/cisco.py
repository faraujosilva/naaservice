from src.device.base import BaseDevice
from src.models.device_models import CPUUsage, Interfaces
from typing import List

class Cisco(BaseDevice):
    def __init__(self, name: str, ip: str, type:str, port:int, vendor: str, os: str, driver: str=None):
        super().__init__(name, ip, type, port, vendor, os, driver)
        
    def get_cpu_usage(self) -> CPUUsage:
        return super().get_cpu_usage()
    
    def get_interfaces(self) -> List[Interfaces]:
        return super().get_interfaces()