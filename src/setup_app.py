import os
import json
from os import getenv
from flask import request, jsonify, current_app as app
from src.engine.engine import Engine
from src.database.mongodb import MongoDB
from src.models.models import Drivers
from src.engine.parser import Parser
from src.connector.conector_factory import ConnectorFactory
from src.device.device_factory import DeviceFactory
from src.driver.driver_factory import DriverFactory

def create_endpoint(blueprint, endpoint, method, data, file_name):
    unique_endpoint_name = (
        f"{file_name}_{endpoint.replace('/', '_').strip('_')}_{method.lower()}"
    )

    @blueprint.route(endpoint, methods=[method], endpoint=unique_endpoint_name)
    def generic_endpoint():
        parameters = data["endpoint"]["parameters"]
        for parameter, attrs in parameters.items():
            if attrs["required"] and parameter not in request.args:
                return jsonify({"error": f"Parameter {parameter} is required"}), 400
        try:
            driver = DriverFactory(Drivers(**data["drivers"]))
            db = MongoDB(
                app.config["mongo_db"],
                app.config["mongo_collection"],
                app.config["mongosc"],
            )
            connector = ConnectorFactory()
            device_factory = DeviceFactory()
            credentials = {
                "username": getenv("AUTOMATION_USER", request.args.get('username')),
                "password": getenv("AUTOMATION_PASS", request.args.get('password')),
                "community": getenv("AUTOMATION_COMMUNITY", request.args.get('community'))
            }
            device = device_factory.create_device(request.args.get("device_ip"), db, connector, credentials)
            engine = Engine()
            engine = engine.create(db, driver, device, connector, Parser()
            )
            # print(f"Engine loaded with {len(device)} devices")
            resp, code = engine.run()
            return jsonify(resp), code
        except Exception as e:
            return jsonify({"error": str(e)}), 500


def load_endpoints(blueprint, directory):
    for subfolder in os.listdir(directory):
        folder_path = os.path.join(directory, subfolder)
        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                if file.endswith(".json"):
                    file_path = os.path.join(folder_path, file)
                    with open(file_path, "r") as f:
                        data = json.load(f)
                        endpoint = data["endpoint"]["name"]
                        method = data["endpoint"]["method"]
                        create_endpoint(
                            blueprint, endpoint, method, data, file.replace(".json", "")
                        )

