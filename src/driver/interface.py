from abc import ABC, abstractmethod
from typing import Union, List
from src.models.models import SSHDriver, APIDriver, SNMPDriver
from src.connector.interface import IConnector
from src.device.interface import IDevice
from src.models.models import Command


class IDriver(ABC):
    @abstractmethod
    def get_driver(self, device_driver: str) -> Union[SSHDriver, APIDriver, SNMPDriver]:
        pass

    @abstractmethod
    def get_driver_order(self) -> list:
        pass

    @abstractmethod
    def run(
        self,
        device: IDevice,
        credentials: dict,
        connector: IConnector,
        connector_name: str,
    ):
        pass

    def get_commands(self, device: IDevice, connector_name: str) -> List[Command]:
        pass
