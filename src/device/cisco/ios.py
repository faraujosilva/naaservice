from src.device.interface import IRouter, ISwitch
from src.device.base import BaseDevice
from src.device.cisco.base import BaseCiscoDevice
from src.connector.interface import IConnector

class IOSSwitch(BaseCiscoDevice, ISwitch):
    def __init__(self, ip, name, type, port, vendor, os, driver='', connector: IConnector = None):
        super().__init__(ip, name, type, port, vendor, os, driver, connector)
        self.BASE = 'IOS Base'

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

    def get_vlans(self):
        return 'SSH IOS: show vlan br'
    
class IOSRouter(BaseCiscoDevice, IRouter):
    def __init__(self, ip, name, type, port, vendor, os, driver='', connector: IConnector = None):
        super().__init__(ip, name, type, port, vendor, os, driver, connector)
        self.BASE = 'IOS Base'

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
        return 'SSH IOS: show ip route'
