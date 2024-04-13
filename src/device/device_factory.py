from typing import List
from src.device.cisco import Cisco
from src.device.interface import IDevice
from src.database.interface import IDatabase


CLASS_MAP = {"cisco": Cisco}


class DeviceFactory:
    def create_device(self, device_ip: str, db: IDatabase) -> List[IDevice]:
        _query = {"ip": device_ip} if device_ip is not None else {}
        ##print(f"Querying device {device_ip}")
        db_devices = list(db.get(_query))
        # devs = [Cisco(**device) for device in db_devices] if len(db_devices) > 0 else None
        devs = []
        for device in db_devices:
            device_type = device.get("vendor").lower()
            device_class = CLASS_MAP.get(device_type)
            if device_class is None:
                raise Exception(f"Device type {device_type} not found")
            devs.append(device_class(**device))
        if devs is None:
            raise Exception(f"Device {device_ip} not found")
        return devs
