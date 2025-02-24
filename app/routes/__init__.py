from flask import Blueprint

from .main_routes import main_routes

def register_blueprints(app):
    app.register_blueprint(main_routes, url_prefix="/")