
from src.models.models import Drivers, DriverOrder, SSHDriver, APIDriver, SNMPDriver
from src.connector.interface import IConnector
from src.device.interface import IDevice
from src.engine.parser import Parser
from src.models.models import Command
from src.driver.interface import IDriver
from typing import Union

class DriverFactory(IDriver):

    def __init__(self, drivers: Drivers):
        self.drivers = drivers
        
    def get_driver(self, device_driver: str = None) -> Union[SSHDriver, APIDriver, SNMPDriver]:
        order = self.drivers.order if self.drivers.order is not None else [driver.name for driver in DriverOrder]
        if not self.drivers.order:
            order.sort(key=lambda x: DriverOrder[x].value)
        
        if device_driver is not None:
            order = [device_driver]
        
        for driver_name in order:
            if self.drivers.model_dump().get(driver_name) is None:
                continue
            driver = self.drivers.model_dump().get(driver_name)
            if driver_name == DriverOrder.ssh.name:
                return SSHDriver(**driver)
            elif driver_name == DriverOrder.api.name:
                return APIDriver(**driver)
            elif driver_name == DriverOrder.snmp.name:
                return SNMPDriver(**driver)
            
    def get_driver_order(self) -> list:
        order = self.drivers.order if self.drivers.order is not None else [driver.name for driver in DriverOrder]
        if not self.drivers.order:
            order.sort(key=lambda x: DriverOrder[x].value)
        return order
    
    def run(self, device: IDevice, commands: Command, parser: Parser, credentials: dict, connector: IConnector):
        return connector.run(device, commands, parser, credentials)