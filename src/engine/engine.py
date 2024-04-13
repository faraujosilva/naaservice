import json
from typing import List, Tuple
from src.driver.interface import IDriver
from src.device.interface import IDevice
from src.models.models import RequestParam, ConnectorOutput, ResultOutput, DeviceOutput, CommandStatus
from src.engine.parser import Parser
from src.connector.conector_factory import ConnectorFactory
from src.database.interface import IDatabase
from os import getenv

class Engine:
    def __init__(self):
        self.request_param = {}
        self.db = None
        self.drivers = None
        self.devices = None
        self.connector_factory = None
        self.parser = None

    def create(self, request_param: RequestParam, db: IDatabase, drivers: IDriver, devices: List[IDevice], connector_factory: ConnectorFactory, parser: Parser) -> 'Engine':
        if not request_param:
            raise ValueError("Request parameters are required")
        
        if not db:
            raise ValueError("Database is required")
        
        if not drivers:
            raise ValueError("Drivers are required")
        
        if not devices:
            raise ValueError("Devices are required")
        
        if not connector_factory:
            raise ValueError("Connector factory is required")
        
        if not parser:
            raise ValueError("Parser is required")
        
        setattr(self, 'request_param', request_param)
        setattr(self, 'db', db)
        setattr(self, 'drivers', drivers)
        setattr(self, 'devices', devices)
        setattr(self, 'connector_factory', connector_factory)
        setattr(self, 'parser', parser)
        return self


    def run(self) -> Tuple[dict, int]:
        credentials = {
            'username': getenv('AUTOMATION_USER', self.request_param.username),
            'password': getenv('AUTOMATION_PASS', self.request_param.password),
            'community': getenv('AUTOMATION_COMMUNITY', self.request_param.community)
        }
        result_output = ResultOutput(device_data=[])
        
        driver_order = self.drivers.get_driver_order()
        
        for device in self.devices:
            device_ip = device.get_ip()
            #print(f"Running device {device_ip}")
            device_output = DeviceOutput(device_info=device.to_dict(), stdout=[], stderr=[])
            success = False
            priority_driver = device.get_driver()
            #print(f"Device {device_ip} has priority driver {priority_driver}")
            
            if priority_driver:
                ordered_drivers = [priority_driver] + [d for d in driver_order if d != priority_driver]
            else:
                ordered_drivers = driver_order
            #print(f"Ordered drivers: {ordered_drivers}")

            for driver_name in ordered_drivers:
                driver = self.drivers.get_driver(driver_name)
                if not driver or success: continue
                #print(f"Driver {driver_name} loaded")
                driver = driver.model_dump()
                device.set_driver(driver_name)

                if not driver:
                    #print(f"Driver {driver_name} is empty")
                    continue
                for connector_name in driver:
                    #print(f"Trying connector {connector_name} for {device_ip}")
                    if success: break
                    if driver[connector_name] is None:
                        #print(f"Driver {driver_name} has no commands for {connector_name}")
                        continue
                    try:
                        commands = self.drivers.get_commands(device, connector_name)
                    except ValueError as e:
                        device_output.stderr.append(CommandStatus(command_name='No command run', output=str(e), status='error'))
                        success = False
                        continue

                    for os_command in commands:
                        if device.get_os() == os_command.os:
                            #print(f"Trying connector {connector_name} for {device_ip}")
                            self.drivers.update_commands(os_command)
                            output: ConnectorOutput = self.drivers.run(device, credentials, self.connector_factory.create_connector(connector_name))
                            if output.error != '':
                                #print(f"Error running {os_command.command_name} for {device_ip}")
                                success = False
                                #This is to try to run all drivers/connector for device, but if all fails, it will return the last error
                                device_output.stderr.append(CommandStatus(command_name=os_command.command_name, output=output.error, status='error'))
                                success = False
                                continue
                            else:
                                #Check if for this IP have a stderr, if yes, remove because have a success command and check if driver was changed
                                if len(device_output.stderr) > 0:
                                    device_output.stderr = []
                                    device.set_driver(driver_name)
                                    device_output.device_info.update({'driver': driver_name})
                                parsed_output = self.parser.parse_output(output.output, os_command.parse, os_command.group)
                                device_output.stdout.append(CommandStatus(command_name=os_command.command_name, output=parsed_output, status='success'))
                                success = True
                            if not device_output.device_info.get('driver', None):
                                device_output.device_info['driver'] = driver_name       
            result_output.device_data.append(device_output)  
        return result_output.model_dump(), 200
