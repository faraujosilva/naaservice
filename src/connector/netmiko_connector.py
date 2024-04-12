from netmiko import ConnectHandler
from netmiko.snmp_autodetect import SNMPDetect
from netmiko.ssh_autodetect import SSHDetect
from netmiko.exceptions import NetMikoTimeoutException, NetMikoAuthenticationException, NetMikoTimeoutException
from src.engine.parser import Parser
from src.device.device import Device
from src.connector.interface import IConnector
from src.models.models import Command
from src.connector.utils import netmiko_commandError

GLOBAL_DRIVER_CACHING = {}

class NetmikoConnector(IConnector):
    def run(self, device: Device, command_detail: Command, parser: Parser, credentials: dict) -> dict:
        if not credentials.get('username') or not credentials.get('password'):
            return {
                "error": "Username and password are required"
            }
        print(f"Running Netmiko driver for {device.get_ip()} with command {command_detail.command}")
        net_device = {
            "device_type": 'autodetect', # or 'cisco_ios
            "host": device.get_ip(),
            "username": credentials.get('username'),
            "password": credentials.get('password'),
        }
        
        if GLOBAL_DRIVER_CACHING.get(device.get_ip()):
            print('Using cache')
            net_device['device_type'] = GLOBAL_DRIVER_CACHING[device.get_ip()]
        else:
            if credentials.get('community'):
                print('Discovering using SNMP')
                try:
                    snmp_detect = SNMPDetect(hostname=device.get_ip(), snmp_version='v2c', community=credentials.get('community'))
                    best_match = snmp_detect.autodetect()
                    if best_match:
                        net_device["device_type"] = best_match
                        GLOBAL_DRIVER_CACHING[device.get_ip()] = best_match
                except Exception:
                    return {
                        "error": "Error in autodetecting device type"
                    }
            else:
                print('Discovering using SSH')
                try:
                    ssh_Detect = SSHDetect(**net_device)
                    best_match = ssh_Detect.autodetect()
                    
                    if best_match:
                        net_device["device_type"] = best_match
                        GLOBAL_DRIVER_CACHING[device.get_ip()] = best_match
                except NetMikoTimeoutException:
                    return {
                        "error": "Timeout in autodetecting device type"
                    }
                except NetMikoAuthenticationException:
                    return {
                        "error": "Authentication error in autodetecting device type"
                    }
                except Exception:
                    return {
                        "error": "General error in autodetecting device type"
                    }
        try:
            with ConnectHandler(**net_device) as net_connect:
                output = net_connect.send_command(command_detail.command).strip()
                if netmiko_commandError(output):
                    return {
                        "error": f"Command: {command_detail.command} ran with error: {output}"
                    }
                
        except NetMikoTimeoutException:
            return {
                "error": "Timeout in connecting to device"
            }
        except NetMikoAuthenticationException:
            return {
                "error": "Authentication error in connecting to device"
            }
        except Exception:
            return {
                "error": "General error in connecting to device"
            }
                
        return {
            "output": parser.parse(output, command_detail.parse, command_detail.group)
        }
    
