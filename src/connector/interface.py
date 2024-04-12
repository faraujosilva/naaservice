from abc import ABC, abstractmethod
from src.device.interface import IDevice
from src.models.models import Command, ConnectorOutput

class IConnector(ABC):
    @abstractmethod
    def run(self, device: IDevice, command_detail: Command, credentials: dict) -> ConnectorOutput:
        pass
