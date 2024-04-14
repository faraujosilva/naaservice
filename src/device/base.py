from src.device.interfaces import IDevice

class BaseDevice(IDevice):
    def __init__(self, ip: str, name: str, type: str, port: int, vendor: str, os: str, driver:str =None):
        self._ip = ip
        self._name = name
        self._d_type = type
        self._port = port
        self._vendor = vendor
        self._os = os
        self._driver = driver
        self._credentials = {}
        #TODO colocar driver
        self.BASE = 'Base Device'

    @property
    def IP(self):
        return self._ip
    
    @property
    def NAME(self):
        return self._name
    
    @property
    def TYPE(self):
        return self._d_type
    
    @property
    def PORT(self):
        return self._port
    
    @property
    def VENDOR(self):
        return self._vendor
    
    @property
    def OS(self):
        return self._os
    
    @property
    def DRIVER(self):
        return self._driver
    
    @property
    def CREDENTIALS(self):
        return self._credentials
    
    @property
    def to_dict(self):
        return {
            "ip": self.IP,
            "name": self.NAME,
            "type": self.TYPE,
            "port": self.PORT,
            "vendor": self.VENDOR,
            "os": self.OS,
            "driver": self.DRIVER,
        }
    
    def set_credentials(self, credentials: dict):
        self._credentials = credentials

    def set_driver(self, driver: str):
        self._driver = driver