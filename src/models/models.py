from typing import Dict, List, Union, Optional
from pydantic import BaseModel
from enum import Enum

class Command(BaseModel):
    vendor: str
    os: str
    type: str
    command_name: str
    command: str
    headers: Optional[Dict[str, str]] = None
    field: Optional[str] = None
    parse: str
    group: int
    
class SNMPDriver(BaseModel):
    pysnmp: Optional[List[Command]] = None

class SSHDriver(BaseModel):
    netmiko: Optional[List[Command]] = None
    ansible: Optional[List[Command]] = None
    
class APIDriver(BaseModel):
    rest: Optional[List[Command]] = None
    restconf: Optional[List[Command]] = None

class Drivers(BaseModel):
    order: Optional[List[str]] = None
    ssh: Optional[SSHDriver] = None
    api: Optional[APIDriver] = None
    snmp: Optional[SNMPDriver] = None

class DriverOrder(Enum):
    snmp = 1
    api = 3
    ssh = 2
    restconf = 4
    netconf = 5
    