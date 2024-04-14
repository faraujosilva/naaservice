from src.device.base import BaseDevice
from src.connector.interface import IConnector

class BaseCiscoDevice(BaseDevice):
    def __init__(self, ip: str, name: str, type: str, port: int, vendor: str, os: str, driver: str = '', connector: IConnector = None):
        super().__init__(ip, name, type, port, vendor, os, driver)
        self.connector = connector