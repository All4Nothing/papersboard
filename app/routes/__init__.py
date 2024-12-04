from flask import Blueprint

# 각 라우트를 import
from .main_routes import main_routes
from .paper_routes import paper_routes
from .user_routes import user_routes

# Blueprint를 등록하기 위한 리스트를 제공
def register_blueprints(app):
    """
    모든 라우트를 Flask 애플리케이션에 등록합니다.
    """
    app.register_blueprint(main_routes, url_prefix="/")
    app.register_blueprint(paper_routes, url_prefix="/papers")
    app.register_blueprint(user_routes, url_prefix="/users")