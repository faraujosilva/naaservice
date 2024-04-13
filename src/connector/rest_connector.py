import json
from os import getenv
import requests
from src.connector.interface import IConnector
from src.device.interface import IDevice
from src.utils.utils import placeholder_device_ip, get_nested_value
from src.models.models import Command, ConnectorOutput


class RestConnector(IConnector):
    """Implementation of IConnector using requests as the underlying library"""
    def run(self, device: IDevice, command_detail: Command, credentials):
        """ Implementation method for IConnector interface"""
        if device.get_os() in CLASS_REST_MAPPING:
            return CLASS_REST_MAPPING[device.get_os()]().run(
                device, command_detail, credentials
            )
        return None  # TODO: Implement default HTTP request here, this is not particular for vendor or something


class ViptelaRestConnector(RestConnector):
    def run(self, device: IDevice, command_detail: Command, credentials):
        ##print(f"Running Viptela driver for {device.get_ip()} with command {command_detail.command}")
        credentials = {
            "vmanage_ip": getenv("VMANAGE_IP", credentials.get("vmanage_ip")),
            "j_username": getenv("VMANAGE_USER", credentials.get("j_username")),
            "j_password": getenv("VMANAGE_PASS", credentials.get("j_password")),
        }
        if (
            not credentials.get("vmanage_ip")
            or not credentials.get("j_username")
            or not credentials.get("j_password")
        ):
            return ConnectorOutput(
                error="VMANAGE_IP, VMANAGE_USER and VMANAGE_PASS are required"
            )

        self.session = {}
        try:
            self.__login(
                credentials.get("vmanage_ip"),
                credentials.get("j_username"),
                credentials.get("j_password"),
            )
        except Exception as err_stats:
            return ConnectorOutput(error=str(err_stats))
        endpoint = placeholder_device_ip(command_detail.command, device.get_ip())

        req = self.__get_request(endpoint, credentials.get("vmanage_ip"))

        if req is not None:
            req = req.decode("utf-8")
            data = json.loads(req)
            field_value = get_nested_value(data, command_detail.field)
            return ConnectorOutput(output=field_value)
        return ConnectorOutput(error="No data found")

    def __login(self, vmanage_ip, username, password):
        """Login to vmanage"""
        base_url_str = "https://%s/" % vmanage_ip

        login_action = "/j_security_check"

        # Format data for loginForm
        login_data = {"j_username": username, "j_password": password}

        # Url for posting login data
        login_url = base_url_str + login_action
        sess = requests.session()

        # If the vmanage has a certificate signed by a trusted authority change verify to True
        login_response = sess.post(url=login_url, data=login_data, verify=False)

        if b"<html>" in login_response.content:
            # print ("Login Failed")
            sess.close()
            raise Exception("Login Failed at vitptela")

        self.session[vmanage_ip] = sess

    def __get_request(self, mount_point, vmanage_ip):
        """GET request"""
        url = "https://%s/dataservice/%s" % (vmanage_ip, mount_point)
        ##print url
        response = self.session[vmanage_ip].get(url, verify=False)
        data = response.content
        self.session[vmanage_ip].close()
        return data


class AciRestConnector(RestConnector):
    def run(self, device: IDevice, command_detail: Command, credentials: dict):
        """ Implementation method for IConnector interface"""

CLASS_REST_MAPPING = {
    "viptela": ViptelaRestConnector,
    "aci": AciRestConnector,
}
