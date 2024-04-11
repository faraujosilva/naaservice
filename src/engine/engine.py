from typing import List
from src.driver.interface import IDriver
from src.device.interface import IDevice
from src.models.models import Command
from src.engine.parser import Parser
from src.connector.interface import IConnector
from src.database.interface import IDatabase
from os import getenv

class Engine:
    def __init__(self, request_param: dict, db: IDatabase, drivers: IDriver, devices: List[IDevice], connector: IConnector, parser: Parser):
        self.request_param = request_param
        self.drivers = drivers
        self.devices = devices
        self.connector = connector
        self.parser = parser
        self.db = db
    
    def run(self) -> List[dict]:
        credentials = {
            'username': self.request_param.get('username', getenv('AUTOMATION_USER')),
            'password': self.request_param.get('password', getenv('AUTOMATION_PASS')),
            'community': self.request_param.get('community', getenv('AUTOMATION_COMMUNITY'))
        }
        combined_output = []
        
        driver_order = self.drivers.get_driver_order()
        for device in self.devices:
            success = False
            priority_driver = device.get_driver()
            if priority_driver and priority_driver in driver_order:
                ordered_drivers = [priority_driver] + [d for d in driver_order if d != priority_driver]
            else:
                ordered_drivers = driver_order
            for driver_name in ordered_drivers:
                driver = self.drivers.get_driver(driver_name).model_dump()
                device.set_driver(driver_name)
                if len(driver) > 0:
                    for connector_name in driver:
                        print(f"Trying connector {connector_name} for {device.get_ip()}")
                        if success: break
                        if driver[connector_name] is None:
                            print(f"Driver {driver_name} has no commands for {connector_name}")
                            break
                        count_os = sum(1 for entry in driver[connector_name] if entry.get('os') == device.get_os() and entry.get('type') == device.get_type())
                        for os_command in driver[connector_name]:
                            if device.get_os() == os_command.get('os'):
                                output = {}
                                connector = self.connector.create_connector(connector_name)
                                output = connector.run(device, Command(**os_command), self.parser, credentials)
                                if output.get('error'):
                                    success = False
                                    continue
                                if count_os == 1:
                                    combined_output.append({
                                        **device.__dict__,
                                        os_command['command_name']: output.get('output')
                                    })
                                    success = True
                                    break
                                else:
                                    for entry in combined_output:
                                        if entry['ip'] == device.get_ip():
                                            entry[os_command['command_name']] = output.get('output')
                                            success = True
                                            break
                                    else:
                                        combined_output.append({
                                            **device.to_dict(),
                                            os_command['command_name']: output.get('output')
                                        })
                                        success = True
                else:
                    print(f"Driver {driver_name} is empty")
        return combined_output, 200
    
