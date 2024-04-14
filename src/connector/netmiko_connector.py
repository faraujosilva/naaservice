import logging
from netmiko import ConnectHandler
from src.models.m_errors import BaseErrors, NetmikoErrors
from netmiko.snmp_autodetect import SNMPDetect
from netmiko.ssh_autodetect import SSHDetect
from netmiko.exceptions import (
    NetMikoTimeoutException,
    NetMikoAuthenticationException,
    NetMikoTimeoutException,
)
from src.device.interface import IDevice
from src.connector.interface import IConnector
from src.models.models import Command, ConnectorOutput
from src.utils.utils import netmiko_commandError

# Set up logging to only display critical errors for Paramiko and Netmiko
logging.getLogger("paramiko").setLevel(logging.CRITICAL)  # No tracebacks for Paramiko
logging.getLogger("netmiko").setLevel(logging.CRITICAL)  # No tracebacks for Netmiko

GLOBAL_DRIVER_CACHING = {}


class NetmikoConnector(IConnector):
    """Implementation of IConnector using Netmiko as the underlying library"""
    def __try_ssh_autodetect(self, ssh_detect: SSHDetect):
        best_match = 'cisco_ios'
        try:
            best_match = ssh_detect.autodetect()
        except NetMikoTimeoutException:
            return ConnectorOutput(error=NetmikoErrors.TIMEOUT_ERROR)
        except NetMikoAuthenticationException:
            return ConnectorOutput(
                error=BaseErrors.CREDENTIAL_ERROR
            )
        except Exception:
            return ConnectorOutput(
                error=NetmikoErrors.GENERAL_NETMIKO_ERROR
            )
        return best_match
            
    def run(
        self, device: IDevice, command_detail: Command
    ) -> ConnectorOutput:
        """ Implementation metdod for IConnector interface"""
        try:
            device.CREDENTIALS.get("username"), device.CREDENTIALS.get("password"), device.CREDENTIALS.get("community")
        except Exception:
            return ConnectorOutput(error=BaseErrors.CREDENTIAL_ERROR)
        net_device = {
            "device_type": "autodetect",  # or 'cisco_ios
            "host": device.get_ip(),
            "username": device.CREDENTIALS.get("username"),
            "password": device.CREDENTIALS.get("password"),
        }

        if GLOBAL_DRIVER_CACHING.get(device.get_ip()):
            ##print('Using cache')
            net_device["device_type"] = GLOBAL_DRIVER_CACHING[device.get_ip()]
        else:
            if device.CREDENTIALS.get("community"):
                ##print('Discovering using SNMP')
                try:
                    snmp_detect = SNMPDetect(
                        hostname=device.get_ip(),
                        snmp_version="v2c",
                        community=device.CREDENTIALS.get("community"),
                    )
                    best_match = snmp_detect.autodetect()
                    if best_match:
                        net_device["device_type"] = best_match
                        GLOBAL_DRIVER_CACHING[device.get_ip()] = best_match
                except Exception:
                    try:
                        detect_ssh = SSHDetect(**net_device)
                        best_match = self.__try_ssh_autodetect(detect_ssh(**net_device))
                        if best_match:
                            net_device["device_type"] = best_match
                            GLOBAL_DRIVER_CACHING[device.get_ip()] = best_match
                    except Exception:
                        return ConnectorOutput(error=NetmikoErrors.DETECTION_ERROR)
            else:
                try:
                    detect_ssh = SSHDetect(**net_device)
                    best_match = self.__try_ssh_autodetect(detect_ssh(**net_device))
                    if best_match:
                        net_device["device_type"] = best_match
                        GLOBAL_DRIVER_CACHING[device.get_ip()] = best_match
                except Exception:
                    return ConnectorOutput(error=NetmikoErrors.SSH_DETECT_ERROR)
        try:
            with ConnectHandler(**net_device) as net_connect:
                # test if have exception connecthandler
                output = net_connect.send_command(command_detail.command).strip()
                if netmiko_commandError(output):
                    return ConnectorOutput(
                        error=f"Command: {command_detail.command} ran with error: {output}"
                    )
        except NetMikoTimeoutException:  # This is instance for paramiko errors
            return ConnectorOutput(error=NetmikoErrors.TIMEOUT_ERROR)
        
        except NetMikoAuthenticationException: 
            return ConnectorOutput(error=NetmikoErrors.AUTH_ERROR)

        except Exception:
            return ConnectorOutput(error=NetmikoErrors.GENERAL_NETMIKO_ERROR)

        return ConnectorOutput(output=output)
