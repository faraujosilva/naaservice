from typing import Union
from src.connector.netmiko_connector import NetmikoConnector
from src.connector.snmp_connector import SNMPConnector
from src.connector.rest_connector import RestConnector


class ConnectorFactory:
    def __init__(self):
        self.connectors = {
            "netmiko": NetmikoConnector(),
            "pysnmp": SNMPConnector(),
            "rest": RestConnector(),
        }
    def create_connector(
        self, connector_name: str
    ) -> Union[NetmikoConnector, SNMPConnector, RestConnector]:
        if connector_name not in self.connectors:
            raise Exception(f"Connector {connector_name} not found")
        return self.connectors.get(connector_name)
