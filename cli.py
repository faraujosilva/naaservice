import argparse
import os
import json
from dotenv import load_dotenv
from os import getenv
from src.engine.engine import Engine
from src.database.mongodb import MongoDB
from src.device.device_factory import DeviceFactory
from src.engine.engine import Engine
from src.models.models import Drivers, RequestParam
from src.engine.parser import Parser
from src.connector.conector_factory import ConnectorFactory
from src.device.device_factory import DeviceFactory
from src.driver.driver_factory import DriverFactory

def load_cli_endpoint(directory, service_name):
    for file in os.listdir(directory):
        for subfolder in os.listdir(directory):
            folder_path = os.path.join(directory, subfolder)
            if os.path.isdir(folder_path):
                for file in os.listdir(folder_path):
                    if file.endswith(".json"):
                        file_path = os.path.join(folder_path, file)
                        with open(file_path, 'r') as f:
                            service = json.load(f)
                        if service.get('service_name') == service_name:
                            return service
    return None

class CLI(Engine):
    def __init__(self, request_param: RequestParam, device_factory: DeviceFactory, db: MongoDB, driver: DriverFactory, connector: ConnectorFactory, parser: Parser):
        self.request_param = request_param
        self.device_factory = device_factory
        self._devices = []
        self.db = db
        self.driver = driver
        self.connector = connector
        self.parser = parser
        
        self.__load_engine()
        
    def __load_engine(self):
        if isinstance(self.request_param.device_ip, list):
            for device_ip in self.request_param.device_ip:
                self._devices = self.device_factory.create_device(device_ip, self.db)
        else:
            self._devices = self.device_factory.create_device(self.request_param.device_ip, self.db)
        self.create(self.request_param, self.db, self.driver, self._devices, self.connector, self.parser)
    
            
        
if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser(description='CLI for network automation')
    parser.add_argument('--device_ip', type=str, help='Device IP and multiple IPs separated by comma')
    parser.add_argument('--mongo_database', type=str, help='Mongo database')
    parser.add_argument('--mongo_collection', type=str, help='Mongo collection')
    parser.add_argument('--mongo_sc', type=str, help='Mongo SC')
    parser.add_argument('--output', type=str, help='Output format, default is JSON')
    parser.add_argument('--output_filter', type=str, help='Filter output')
    parser.add_argument('--service', type=str, help='Service to run')
    args = parser.parse_args()
    
    if not args.service:
        parser.error("Please set service using --service")
        
    if not args.device_ip:
       args.device_ip = None

    if args.device_ip is not None and (',' in args.device_ip or ', ' in args.device_ip):
        args.device_ip = args.device_ip.split(',')
        
    if not getenv('MONGO_DB') or not getenv('MONGO_COLLECTION') or not getenv('MONGO_SC'):
        if not args.mongo_database or not args.mongo_collection or not args.mongo_sc:
            parser.error("Please set MONGO_DB, MONGO_COLLECTION and MONGO_SC environment variables or setup using --mongo_database, --mongo_collection and --mongo_sc")
    db = MongoDB(getenv('MONGO_DB', args.mongo_database), getenv('MONGO_COLLECTION', args.mongo_collection), getenv('MONGO_SC', args.mongo_sc))
    device_factory = DeviceFactory()
    
    service = load_cli_endpoint('./services', args.service)
    if not service:
        parser.error("Service not found or service name not provided at configuration file")

    driver = DriverFactory(Drivers(**service['drivers']))
    connector = ConnectorFactory()
    cli = CLI(RequestParam(**args.__dict__), device_factory, db, driver, connector, Parser())
    
    print(cli.run())