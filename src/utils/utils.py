import re

def placeholder_device_ip(string: str, device_ip: str) -> str:
    """Replace the string {{ device_ip }} or {{{device_ip}} with the device ip"""
    return re.sub(r'\{\{\s*device_ip\s*\}\}', device_ip, string)

def get_nested_value(data_to_search, key_path):
    """
    Get the value a expression "field": "data[0].cpu_user
    key is "data[0].cpu_user" or "data.cpu_user" or "data"
    data_to_search is the data to search, can be a dict or list
    { device_data: [{'device_info': {'name': 'RT02', 'ip': '192.168.244.139', 'port': '22', 'type': 'router', 'vendor': 'cisco', 'os': 'ios', 'driver': 'snmp'}, 'stdout': [{'command_name': 'cpu_usage', 'output': '0', 'status': 'success'}], 'stderr': []}]}
    """
    current_element = data_to_search
    parts = key_path.split('.')
    try:
        for part in parts:
            #check if is a list
            if isinstance(current_element, list):
                if isinstance(current_element[0], list):
                    current_element = current_element[0]
                current_element = [elem.get(part) for elem in current_element]
                for elem in current_element:
                    #[[{'command_name': 'cpu_usage', 'output': '0', 'status': 'success'}]]
                    if isinstance(elem, list):
                        for e in elem:
                            if part in e:
                                current_element = e[part]
                    
            else:
                current_element = current_element[part]
    except (KeyError, IndexError, TypeError):
        return None  # Retorna None se algum caminho não for encontrado ou ocorrer erro de tipo

    if isinstance(current_element, list) and len(current_element) == 1:
        return current_element[0]
    return current_element


def netmiko_commandError(output: str) -> bool:
    """Check if the output is a netmiko error"""
    if "^\n% Invalid input detected at '^' marker.\n" in output:
        return True
    if 'Invalid input detected' in output:
        return True
    return False