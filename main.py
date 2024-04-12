import logging
from flask import Flask, Blueprint
from os import getenv
from dotenv import load_dotenv
from src.setup_app import load_endpoints

dynamic_endpoints = Blueprint('dynamic_endpoints', __name__)

load_endpoints(dynamic_endpoints, directory="./services")

app = Flask(__name__)
app.register_blueprint(dynamic_endpoints)

if __name__ == "__main__":
    load_dotenv()
    logger = logging.getLogger('werkzeug')
    app.config['logger'] = logger
    app.config['mongosc'] = getenv("MONGO_SC")
    app.config['mongo_db'] = getenv("MONGO_DB")
    app.config['mongo_collection'] = getenv("MONGO_COLLECTION")
    app.run(debug=False, host='0.0.0.0', port=5001, load_dotenv=True)
