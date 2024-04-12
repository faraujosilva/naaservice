from pysnmp.hlapi import *
from src.connector.interface import IConnector
from src.device.device import Device
from src.models.models import Command
from src.engine.parser import Parser

class SNMPConnector(IConnector):
    def run(self, device: Device, command_detail: Command, parser: Parser, credentials: dict) -> dict:
        if not credentials.get('community'):
            return {
                "error": "Community is required"
            }
        print(f"Running SNMP driver for {device.get_ip()} with command {command_detail.command}")
        try:
            # Create SNMP engine
            snmp_engine = SnmpEngine()

            # Define target
            target = UdpTransportTarget((device.get_ip(), 161))

            # Perform SNMP walk (using nextCmd for iteration)
            for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(
                snmp_engine, CommunityData(credentials.get('community')), target, ContextData(), ObjectType(ObjectIdentity(command_detail.command)), lexicographicMode=False
            ):

                if errorIndication:
                    print(f"Error: {errorIndication}")
                    return {
                        "error": errorIndication
                    }

                elif errorStatus:
                    print(f"Error at {errorIndex}: {errorStatus}")
                    return {
                        "error": errorStatus
                    }

                else:
                    # Print OID and value for each response
                    for name, val in varBinds:
                        #Print exatch when running snmpwalk with STRING, INTEGER etc
                        poutput = f"{name} = {val.prettyPrint()}"
                        return {
                            "output": parser.parse(poutput, command_detail.parse, command_detail.group)
                        }

        except Exception as e:
            print(f"Error: {e}")