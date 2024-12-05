from flask import Flask
from flask_cors import CORS
from transformers import pipeline
from app.routes.main_routes import main_routes
from app.routes.paper_routes import paper_routes
from app.routes import register_blueprints
from app.services import initialize_services

import os
import logging

app = Flask(__name__, template_folder=os.path.join("app", "templates"))
CORS(app)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

register_blueprints(app)
initialize_services(app)

if __name__ == "__main__":
    app.run(debug=True)