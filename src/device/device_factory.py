
from typing import List
from src.device.device import Device
from src.database.interface import IDatabase

class DeviceFactory:
    def create_device(self, device_ip: str, db: IDatabase) -> List[Device]:
        _query = {'ip': device_ip} if device_ip is not None else {}
        print(f"Querying device {device_ip}")
        db_devices = list(db.get(_query))
        devs = [Device(**device) for device in db_devices] if len(db_devices) > 0 else None
        if devs is None:
            raise Exception(f"Device {device_ip} not found")
        return devs
        