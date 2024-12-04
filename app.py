from flask import Flask
from app.routes.main_routes import main_routes
from app.routes.paper_routes import paper_routes
from app.routes import register_blueprints
from app.services import initialize_services

import os

app = Flask(__name__, template_folder=os.path.join("app", "templates"))

register_blueprints(app)
initialize_services(app)

if __name__ == "__main__":
    app.run(debug=True)