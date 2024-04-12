from abc import ABC, abstractmethod
from src.device.device import Device
from src.models.models import Command, ConnectorOutput

class IConnector(ABC):
    @abstractmethod
    def run(self, device: Device, command_detail: Command, credentials: dict) -> ConnectorOutput:
        pass
