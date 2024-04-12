from typing import List
from src.driver.interface import IDriver
from src.device.interface import IDevice
from src.models.models import Command
from src.engine.parser import Parser
from src.connector.conector_factory import ConnectorFactory
from src.database.interface import IDatabase
from os import getenv

class Engine:
    def __init__(self, request_param: dict, db: IDatabase, drivers: IDriver, devices: List[IDevice], connector_factory: ConnectorFactory, parser: Parser):
        self.request_param = request_param
        self.drivers = drivers
        self.devices = devices
        self.connector_factory = connector_factory
        self.parser = parser
        self.db = db
    
    def run(self) -> List[dict]:
        credentials = {
            'username': self.request_param.get('username', getenv('AUTOMATION_USER')),
            'password': self.request_param.get('password', getenv('AUTOMATION_PASS')),
            'community': self.request_param.get('community', getenv('AUTOMATION_COMMUNITY'))
        }
        combined_output = []
        last_driver_error = []
        
        driver_order = self.drivers.get_driver_order()
        for device in self.devices:
            success = False
            priority_driver = device.get_driver()
            print(f"Device {device.get_ip()} has priority driver {priority_driver}")
            if priority_driver:
                ordered_drivers = [priority_driver] + [d for d in driver_order if d != priority_driver]
            else:
                ordered_drivers = driver_order
            print(f"Ordered drivers: {ordered_drivers}")
            for driver_name in ordered_drivers:
                driver = self.drivers.get_driver(driver_name)
                if not driver:
                    continue
                print(f"Driver {driver_name} loaded")
                driver = driver.model_dump()
                device.set_driver(driver_name)
                if len(driver) > 0:
                    for connector_name in driver:
                        if success: break
                        if driver[connector_name] is None:
                            print(f"Driver {driver_name} has no commands for {connector_name}")
                            continue
                        count_os = sum(1 for entry in driver[connector_name] if entry.get('os') == device.get_os() and entry.get('type') == device.get_type())
                        print(driver[connector_name])
                        for os_command in driver[connector_name]:
                            if device.get_os() == os_command.get('os'):
                                print(f"Trying connector {connector_name} for {device.get_ip()}")
                                output = {}
                                output = self.drivers.run(device, Command(**os_command), self.parser, credentials, self.connector_factory.create_connector(connector_name))
                                if output.get('error'):
                                    success = False
                                    #This is to try to run all drivers/connector for device, but if all fails, it will return the last error
                                    if len(last_driver_error) > 0:
                                        #append
                                        for entry in last_driver_error:
                                            if entry['ip'] == device.get_ip():
                                                entry['stderr'].append({os_command['command_name']: output.get('error'), 'status': 'error'})
                                                success = False
                                                break
                                    else:
                                        last_driver_error.append({
                                            **device.to_dict(),
                                            'stderr': [
                                                {os_command['command_name']: output.get('error'), 'status': 'error'}
                                            ],
                                        })
                                        success = False
                                    combined_output.extend(last_driver_error)
                                    continue
                                if count_os == 1:
                                    combined_output.append({
                                        **device.to_dict(),
                                        'stdout': [
                                            {os_command['command_name']: output.get('output'), 'status': 'success'},
                                        ],
                                    })
                                    success = True
                                    break
                                else:
                                    for entry in combined_output:
                                        if entry['ip'] == device.get_ip():
                                            entry['stdout'].append({os_command['command_name']: output.get('output'), 'status': 'success'})
                                            success = True
                                            break
                                    else:
                                        combined_output.append({
                                            **device.to_dict(),
                                            'stdout': [
                                                {os_command['command_name']: output.get('output'), 'status': 'success'}
                                            ],
                                        })
                                        success = True
                else:
                    print(f"Driver {driver_name} is empty")
        return combined_output, 200
    
