from pysnmp.hlapi import (
    SnmpEngine,
    UdpTransportTarget,
    CommunityData,
    ContextData,
    nextCmd,
    ObjectType,
    ObjectIdentity,
)
from src.models.m_errors import BaseErrors, SNMPErrors
from pysnmp.proto.rfc1902 import TimeTicks
from datetime import timedelta
from src.connector.interface import IConnector
from src.device.interface import IDevice
from src.models.models import Command, ConnectorOutput


class SNMPConnector(IConnector):
    """Implementation of IConnector using PySNMP as the underlying library"""
    def run(
        self, device: IDevice, command_detail: Command
    ) -> ConnectorOutput:
        """ Implementation method for IConnector interface"""
        try:
            device.CREDENTIALS.get("community")
            print('fefe')
            print(device.CREDENTIALS.get("community"))
        except:
            return ConnectorOutput(error=SNMPErrors.COMMUNITY_ERROR)
        try:
            snmp_engine = SnmpEngine()

            target = UdpTransportTarget((device.get_ip(), 161))

            for error_indication, error_status, _, var_binds in nextCmd(
                snmp_engine,
                CommunityData(device.CREDENTIALS.get("community")),
                target,
                ContextData(),
                ObjectType(ObjectIdentity(command_detail.command)),
                lexicographicMode=False,
            ):
                if error_indication:
                    return ConnectorOutput(error=str(error_indication))

                if error_status:
                    return ConnectorOutput(error=str(error_status))
                for _, val in var_binds:
                    if isinstance(
                        val, TimeTicks
                    ):  # Convert to datetime with days, hours, minutes and seconds based on val.prettyPrint() string
                        ticks = int(val.prettyPrint())
                        delta = timedelta(seconds=ticks / 100)
                        days = delta.days
                        hours, remainder = divmod(delta.seconds, 3600)
                        minutes, _ = divmod(remainder, 60)

                        # Format the output string
                        if days > 0:
                            poutput = (
                                f"{days} days, {hours} hours, {minutes} minutes"
                            )
                        else:
                            poutput = f"{hours} hours, {minutes} minutes"
                        return ConnectorOutput(output=poutput)
                    poutput = val.prettyPrint()
                    return ConnectorOutput(output=poutput)

        except Exception as err_stat:
            print(err_stat)
            return ConnectorOutput(error=f"{SNMPErrors.GENERAL_SNMP_ERROR}: {err_stat}")
