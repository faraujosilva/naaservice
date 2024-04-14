from abc import ABC, abstractmethod
from src.device.interfaces import IDevice
from src.models.models import Command, ConnectorOutput


class IConnector(ABC):
    """Abstract class for all connectors"""

    @abstractmethod
    def run(
        self, device: IDevice, command_detail: Command, credentials: dict
    ) -> ConnectorOutput:
        """_summary_

        Args:
            device (IDevice): device Interface representing the device to connect to
            command_detail (Command): A pydantic model representing the command to run with some metadata
            credentials (dict): A dictionary containing the credentials to connect to the device(username, password, community and more if needed)

        Returns:
            ConnectorOutput: A pydantic model output contains the result of the command
        """
