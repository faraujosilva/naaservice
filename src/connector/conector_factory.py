from typing import Union
from src.connector.netmiko_connector import NetmikoConnector
from src.connector.snmp_connector import SNMPConnector

class ConnectorFactory:
    def create_connector(self, connector_name: str) -> Union[NetmikoConnector, SNMPConnector]:
        if connector_name == 'netmiko':
            from src.connector.netmiko_connector import NetmikoConnector
            return NetmikoConnector()
        elif connector_name == 'pysnmp':
            from src.connector.snmp_connector import SNMPConnector
            return SNMPConnector()
        elif connector_name == 'rest':
            from src.connector.rest_connector import RestConnector
            return RestConnector()
        else:
            raise Exception(f"Connector {connector_name} not found")
        