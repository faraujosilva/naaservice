from src.models.models import Drivers, DriverOrder, SSHDriver, APIDriver, SNMPDriver
from src.connector.interface import IConnector
from src.device.interface import IDevice
from src.models.models import Command
from src.driver.interface import IDriver
from typing import Union, List


class DriverFactory(IDriver):
    def __init__(self, drivers: Drivers):
        self.drivers = drivers
        self.avaliable_drivers = {
            DriverOrder.ssh.name: SSHDriver,
            DriverOrder.api.name: APIDriver,
            DriverOrder.snmp.name: SNMPDriver,
        }
        self.commands: Command = None

    def get_driver(
        self, device_driver: str = None
    ) -> Union[SSHDriver, APIDriver, SNMPDriver]:
        order = (
            self.drivers.order
            if self.drivers.order is not None
            else [driver.name for driver in DriverOrder]
        )
        if not self.drivers.order:
            order.sort(key=lambda x: DriverOrder[x].value)

        if device_driver is not None:
            order = [device_driver]

        for driver_name in order:
            if self.drivers.model_dump().get(driver_name) is None:
                continue
            driver = self.drivers.model_dump().get(driver_name)
            if driver is not None:
                return self.avaliable_drivers[driver_name].parse_obj(driver)
        return None

    def get_driver_order(self) -> list:
        order = (
            self.drivers.order
            if self.drivers.order is not None
            else [driver.name for driver in DriverOrder]
        )
        if not self.drivers.order:
            order.sort(key=lambda x: DriverOrder[x].value)
        return order

    def get_commands(self, device: IDevice, connector_name: str) -> List[Command]:
        driver = device.get_driver()
        drivers_dump = self.drivers.model_dump()
        commands = []
        match_commands = [
            command
            for command in drivers_dump.get(driver).get(connector_name)
            if command.get("vendor") == device.get_vendor()
            and command.get("os") == device.get_os()
            and command.get("type") == device.get_type()
        ]
        if not match_commands:
            raise ValueError(
                f"Commands not found for vendor: {device.get_vendor()} - os: {device.get_os()} - type: {device.get_type()} in {driver} driver"
            )

        for command in drivers_dump.get(driver).get(connector_name):
            if (
                command.get("vendor") == device.get_vendor()
                and command.get("os") == device.get_os()
                and command.get("type") == device.get_type()
            ):
                commands.append(Command(**command))

        return commands

    def update_commands(self, commands: List[Command]):
        self.commands = commands

    def run(self, device: IDevice, credentials: dict, connector: IConnector):
        return connector.run(device, self.commands, credentials)
