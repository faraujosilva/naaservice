from enum import Enum

class NetmikoErrors(Enum):
    TIMEOUT_ERROR = 'Timeout in connection'
    AUTH_ERROR = 'Authentication error in connection'
    GENERAL_NETMIKO_ERROR = 'General error in Netmiko connection'
    DETECTION_ERROR = 'Could not detect device type neither by SNMP nor SSH"'
    SSH_DETECT_ERROR = 'Could not detect device type by SSH'
    
class SNMPErrors(Enum):
    COMMUNITY_ERROR = 'Community string is required for SNMP'
    GENERAL_SNMP_ERROR = 'General error in SNMP connection'

class ViptelaErrors(Enum):
    LOGIN_ERROR = 'Username, password or community and SDWAN data are required'
    NO_DATA_FOUND = 'No data found in the response'

class BaseErrors(Enum):
    CREDENTIAL_ERROR = 'Username, password or community and SDWAN data are required'
