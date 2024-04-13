from typing import Dict, List, Union, Optional, Any
from pydantic import BaseModel
from enum import Enum


class Interfaces(BaseModel):
    intf_name: str
    intf_description: str
    intf_type: str
    intf_mac: str
    intf_ip: str
    intf_mask: str
    intf_status: str
    intf_speed: str
    intf_mtu: str
    intf_bandwidth: str
    intf_delay: str
    intf_reliability: str
    intf_txload: str
    intf_rxload: str
    intf_in_errors: str
    intf_out_errors: str
    intf_in_discards: str
    intf_out_discards: str


class ArpTable(BaseModel):
    mac: str
    ip: str
    intf: str


class Routes(BaseModel):
    network: str
    mask: str
    nexthop: str
    intf: str
    metric: str
    protocol: str


class CPUUsage(BaseModel):
    cpu_1min: str
    cpu_5min: str
