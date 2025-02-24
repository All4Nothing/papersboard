from flask import Flask
from app.services.database import db
from flask_migrate import Migrate
from flask_cors import CORS
from app.routes import register_blueprints
import os

from app.models.paper import Paper

migrate = Migrate()

def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    ROOT_DIR = os.path.dirname(BASE_DIR)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all() 
    
    register_blueprints(app)
    
    return app
