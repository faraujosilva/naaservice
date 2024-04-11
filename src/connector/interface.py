from abc import ABC, abstractmethod
from src.device.device import Device
from src.engine.parser import Parser
from src.models.models import Command

class IConnector(ABC):
    @abstractmethod
    def run(self, device: Device, command_detail: Command, parser: Parser, credentials: dict) -> dict:
        pass