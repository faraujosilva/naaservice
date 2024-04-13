from typing import Dict, List, Union, Optional, Any
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


class CLIDriver(BaseModel):
    device_ip: str
    driver: str
    service: str


class Drivers(BaseModel):
    order: Optional[List[str]] = None
    ssh: Optional[SSHDriver] = None
    api: Optional[APIDriver] = None
    snmp: Optional[SNMPDriver] = None


class RequestParam(BaseModel):
    device_ip: Optional[Union[str, List[str]]] = None
    username: Optional[str] = None
    password: Optional[str] = None
    community: Optional[str] = None
    output: Optional[Any] = None
    output_filter: Optional[str] = None


class ConnectorOutput(BaseModel):
    output: Optional[str] = ""
    error: Optional[str] = ""


class CommandStatus(BaseModel):
    command_name: str
    output: Any
    status: str


class DeviceOutput(BaseModel):
    device_info: Optional[Dict[Optional[str], Optional[str]]] = {}
    stdout: Optional[List[CommandStatus]] = []
    stderr: Optional[List[CommandStatus]] = []


class ResultOutput(BaseModel):
    device_data: List[DeviceOutput]


class DriverOrder(Enum):
    snmp = 1
    api = 3
    ssh = 2
    restconf = 4
    netconf = 5
