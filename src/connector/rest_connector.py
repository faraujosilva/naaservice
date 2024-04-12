import requests
import json
from datetime import datetime
from src.connector.interface import IConnector
from src.device.device import Device
from src.engine.parser import Parser
from src.connector.utils import placeholder_device_ip, get_nested_value
from  src.models.models import Command
from os import getenv

class RestConnector(IConnector):
    def run(self, device: Device, command_detail: Command, parser: Parser, credentials):
        if device.get_os() in CLASS_REST_MAPPING:
            return CLASS_REST_MAPPING[device.get_os()]().run(device, command_detail, parser, credentials)
        else:
            return None #TODO: Implement default HTTP request here, this is not particular for vendor or something

class ViptelaRestConnector(RestConnector):
    def run(self, device: Device, command_detail: Command, parser: Parser, credentials):
        if not credentials.get('vmanage_ip') or not credentials.get('j_username') or not credentials.get('j_password'):
            return {
                "error": "VMANAGE_IP, VMANAGE_USER and VMANAGE_PASS are required"
            }
        print(f"Running Viptela driver for {device.get_ip()} with command {command_detail.command}")
        credentials = {
            "vmanage_ip": getenv("VMANAGE_IP"),
            "j_username": getenv("VMANAGE_USER"),
            "j_password": getenv('VMANAGE_PASS')
        }

        self.session = {}
        try:
            self.__login(credentials.get('vmanage_ip'), credentials.get("j_username"), credentials.get("j_password"))
        except Exception as e:
            return {
                "error": str(e)
            }
        
        endpoint = placeholder_device_ip(command_detail.command, device.get_ip())

        req = self.__get_request(endpoint, credentials.get('vmanage_ip'))
        
        if req is not None:
            req = req.decode('utf-8')
            data = json.loads(req)
            field_value = get_nested_value(data, command_detail.field)
            if command_detail.parse and field_value:
                field_value = parser.parse(field_value, command_detail.parse, command_detail.group)
            return {
                "output": field_value
            }
        return {
            "error": "No data found"
        }

    def __login(self, vmanage_ip, username, password):
        """Login to vmanage"""
        base_url_str = 'https://%s/'%vmanage_ip

        login_action = '/j_security_check'

        #Format data for loginForm
        login_data = {'j_username' : username, 'j_password' : password}

        #Url for posting login data
        login_url = base_url_str + login_action
        sess = requests.session()

        #If the vmanage has a certificate signed by a trusted authority change verify to True
        login_response = sess.post(url=login_url, data=login_data, verify=False)


        if b'<html>' in login_response.content:
            print ("Login Failed")
            sess.close()
            raise Exception("Login Failed at vitptela")

        self.session[vmanage_ip] = sess

    def __get_request(self, mount_point,vmanage_ip):
        """GET request"""
        url = "https://%s/dataservice/%s"%(vmanage_ip, mount_point)
        #print url
        response = self.session[vmanage_ip].get(url, verify=False)
        data = response.content
        self.session[vmanage_ip].close()
        return data

class AciRestConnector(RestConnector):
    def run(self, device, command_detail, parser, credentials):
        pass

CLASS_REST_MAPPING = {
    "viptela": ViptelaRestConnector,
    "aci": AciRestConnector,
}

