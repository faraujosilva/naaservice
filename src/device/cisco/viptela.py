from src.device.interfaces import IRouter
from src.connector.interface import IConnector
from src.device.cisco.base import BaseCiscoDevice

class ViptelaRouter(BaseCiscoDevice, IRouter):
    def __init__(self, ip, name, type, port, vendor, os, driver='', connector: IConnector = None):
        super().__init__(ip, name, type, port, vendor, os, driver, connector)
        self.BASE = 'API Base'
    def get_ip(self):
        return self.IP

    def get_os(self):
        return self.OS

    def get_vendor(self):
        return self.VENDOR

    def get_type(self):
        return self.TYPE

    def get_driver(self):
        return self.DRIVER
        
    def get_routes(self):
        return 'API: /routes/all_vrfs'