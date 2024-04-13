from pysnmp.hlapi import *
from pysnmp.proto.rfc1902 import TimeTicks
from datetime import timedelta, datetime
from src.connector.interface import IConnector
from src.device.interface import IDevice
from src.models.models import Command, ConnectorOutput

class SNMPConnector(IConnector):
    def run(self, device: IDevice, command_detail: Command, credentials: dict) -> ConnectorOutput:
        if not credentials.get('community'):
            return ConnectorOutput(error="Community string is required for SNMP")
        ##print(f"Running SNMP driver for {device.get_ip()} with command {command_detail.command}")
        try:
            snmp_engine = SnmpEngine()

            target = UdpTransportTarget((device.get_ip(), 161))

            for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(
                snmp_engine, CommunityData(credentials.get('community')), target, ContextData(), ObjectType(ObjectIdentity(command_detail.command)), lexicographicMode=False
            ):

                if errorIndication:
                    #print(f"Error: {errorIndication}")
                    return ConnectorOutput(error=errorIndication)

                elif errorStatus:
                    #print(f"Error at {errorIndex}: {errorStatus}")
                    return ConnectorOutput(error=errorStatus)
                else:
                    for name, val in varBinds:
                        if isinstance(val, TimeTicks): #Convert to datetime with days, hours, minutes and seconds based on val.prettyPrint() string
                            ticks = int(val.prettyPrint())
                            delta = timedelta(seconds=ticks/100)
                            days = delta.days
                            hours, remainder = divmod(delta.seconds, 3600)
                            minutes, seconds = divmod(remainder, 60)

                            # Format the output string
                            if days > 0:
                                poutput = f"{days} days, {hours} hours, {minutes} minutes"
                            else:
                                poutput = f"{hours} hours, {minutes} minutes"
                            return ConnectorOutput(output=poutput)
                        else:
                            poutput = val.prettyPrint()
                        return ConnectorOutput(output=poutput)

        except Exception as e:
            ##print(f"General Error: {str(e)}")
            return ConnectorOutput(error=f"General Error: {str(e)}")