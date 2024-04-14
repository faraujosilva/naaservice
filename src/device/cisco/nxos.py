from src.device.interface import IRouter, ISwitch
from src.connector.interface import IConnector
from src.device.cisco.base import BaseCiscoDevice

class NXOSRouter(BaseCiscoDevice, IRouter):
    def __init__(self, ip, name, type, port, vendor, os, driver='', connector: IConnector = None):
        super().__init__(ip, name, type, port, vendor, os, driver, connector)
        self.BASE = 'NXOS Base'

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
        return 'SSH NXOS: show ip route vrf all'
    
class NXOSSwitch(BaseCiscoDevice, ISwitch):
    def __init__(self, ip, name, type, port, vendor, os, driver='', connector: IConnector = None):
        super().__init__(ip, name, type, port, vendor, os, driver, connector)
        self.BASE = 'NXOS Base'
 
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
        return 'SSH NXOS: show vlan all'