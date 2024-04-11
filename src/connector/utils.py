import re

def placeholder_device_ip(string: str, device_ip: str) -> str:
    """Replace the string {{ device_ip }} or {{{device_ip}} with the device ip"""
    return re.sub(r'\{\{\s*device_ip\s*\}\}', device_ip, string)


def get_nested_value(data_to_search: str, keys: list):
    """Get the value a expression "field": "data[0].cpu_user"""
    value = data_to_search
    for key in keys.split('.'):
        #check if have index in the key
        if '[' in key:
            key = key.split('[')
            key[1] = key[1].replace(']', '')
            key[1] = int(key[1])
            value = value[key[0]][key[1]]
            continue
        if key.isdigit():
            key = int(key)
        value = value[key]
    return value