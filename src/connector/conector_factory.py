from typing import Union
from src.connector.netmiko_connector import NetmikoConnector
from src.connector.snmp_connector import SNMPConnector
from src.connector.rest_connector import RestConnector


class ConnectorFactory:
    def create_connector(
        self, connector_name: str
    ) -> Union[NetmikoConnector, SNMPConnector, RestConnector]:
        registry = {
            "netmiko": NetmikoConnector(),
            "pysnmp": SNMPConnector(),
            "rest": RestConnector(),
        }
        if connector_name not in registry:
            raise Exception(f"Connector {connector_name} not found")
        return registry.get(connector_name)
