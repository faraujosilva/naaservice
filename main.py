import os
import json
import logging
from dotenv import load_dotenv
from src.engine.engine import Engine
from src.database.mongodb import MongoDB
from src.models.models import Drivers
from src.engine.parser import Parser
from src.connector.conector_factory import ConnectorFactory
from src.device.device_factory import DeviceFactory
from src.driver.driver_factory import DriverFactory
from flask import Flask, request, jsonify


def create_endpoints(app):
    for subolder in os.listdir("./endpoints"):
        if os.path.isdir(f"./endpoints/{subolder}"):
            for file in os.listdir(f"./endpoints/{subolder}"):
                if file.endswith(".json"):
                    with open(f"./endpoints/{subolder}/{file}") as f:
                        data = json.load(f)
                        endpoint = data['endpoint']['name']
                        method = data['endpoint']['method']
                        print("Endpoint: ", endpoint)
                        print("Method: ", method)
                        def create_endpoint(endpoint, method):
                            @app.route(endpoint, methods=[method])
                            def endpoint_function():
                                parameters = data['endpoint']['parameters']
                                for parameter in parameters:
                                    if parameters[parameter]['required'] and parameter not in request.args:
                                        return jsonify({"error": f"Parameter {parameter} is required"}), 400
                                try:
                                    driver = DriverFactory(Drivers(**data['drivers']))
                                    db = MongoDB(app.config['mongo_db'], app.config['mongo_collection'], app.config['mongosc'])
                                    device_factory = DeviceFactory()
                                    device = device_factory.create_device(request.args.get('device_ip'), db)
                                    connector = ConnectorFactory()
                                    engine = Engine(request.args, db, driver, device, connector, Parser())
                                    resp, code = engine.run()
                                    return jsonify(resp), code
                                    
                                except Exception as e:
                                    app.config['logger'].exception(f"Error at engine level: {e}")
                                    return jsonify({"error": "Internal server error due to: " + str(e)}), 500
                        create_endpoint(endpoint, method)

if __name__ == "__main__":
    app = Flask(__name__)
    load_dotenv()
    create_endpoints(app)
    logger = logging.getLogger('werkzeug')
    app.config['logger'] = logger  
    app.config['mongosc'] = os.getenv("MONGO_SC")
    app.config['mongo_db'] = os.getenv("MONGO_DB")
    app.config['mongo_collection'] = os.getenv("MONGO_COLLECTION")
    app.run(debug=True, host='0.0.0.0', port=5001)