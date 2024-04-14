from typing import Union, List
from src.device.interface import IRouter, ISwitch
from src.database.interface import IDatabase
from src.connector.interface import IConnector
from src.device.cisco.ios import (
    IOSSwitch,
    IOSRouter,
)
from src.device.cisco.nxos import (
    NXOSRouter,
    NXOSSwitch,
)
from src.device.cisco.viptela import ViptelaRouter
from src.device.cisco.ios import IOSSwitch

CLASS_MAP = {
    'cisco': {
        'router': {
            'ios': IOSRouter,
            'nxos': NXOSRouter,
        },
        'switch': {
            'ios': IOSSwitch,
            'nxos': NXOSSwitch
        },
        'sdwan': {
            'viptela': ViptelaRouter
        }
    },
    'juniper': {}
}
class DeviceFactory:
    """
    Create a list of device instances based on the database entries matching the given IP address.
    
    Parameters:
        ip (str): IP address to query the devices.
        db (IDatabase): Database interface to query devices.
        connector (IConnector): Connector interface used for device communication.

    Returns:
        List[Union[IRouter, ISwitch]]: A list of initialized device objects.

    Raises:
        ValueError: If no devices are found for the given IP.
    """
    def create_device(self, ip: str, db: IDatabase, connector: IConnector, credentials: dict) -> List[Union[IRouter, ISwitch]]:
        """ Create a list of device instances based on the database entries matching the given IP address."""
        _query = {"ip": ip} if ip is not None else {}
        db_devices = list(db.get(_query))
        devs = []
        for device in db_devices:
            vendor = device.get('vendor')
            device_type = device.get('type')
            os = device.get('os')
            specific_vendor_class = CLASS_MAP.get(vendor, {}).get(device_type, {}).get(os)
            if specific_vendor_class:
                base_device_args = {k: v for k, v in device.items()}
                base_device_args.update({'connector': connector})
                device_instance = specific_vendor_class(**base_device_args)
                device_instance.set_credentials(credentials)
                devs.append(device_instance)
        if not devs:
            raise ValueError(f"No devices found for IP {ip}")
        return devs