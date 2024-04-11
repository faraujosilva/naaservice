
class ConnectorFactory:
    def create_connector(self, connector_name: str):
        if connector_name == 'netmiko':
            from src.connector.netmiko_connector import NetmikoConnector
            return NetmikoConnector()
        elif connector_name == 'pysnmp':
            from src.connector.snmp_connector import SNMPConnector
            return SNMPConnector()
        elif connector_name == 'ansible':
            from src.connector.ansible_connector import AnsibleConnector
            return AnsibleConnector()
        else:
            raise Exception(f"Connector {connector_name} not found")