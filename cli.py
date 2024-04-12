import argparse
from os import getenv
from src.setup_app import load_cli_endpoints


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CLI for network automation')
    
    if not getenv('MONGO_SC'):
        parser.error('MONGO_SC is required')
        
    if not getenv('MONGO_DB'):
        parser.error('MONGO_DB is required')
    
    if not getenv('MONGO_COLLECTION'):
        parser.error('MONGO_COLLECTION is required')
        
    load_cli_endpoints('./services', definitions)
    parser.add_argument('service', type=str, help='Service to run')
    parser.add_argument('device_ip', type=str, help='Target device IP')
    args = parser.parse_args()
