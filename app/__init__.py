from flask import Flask
from app.services.database import db

def create_app():
    app = Flask(__name__)
    
    # PostgreSQL 데이터베이스 URI 설정
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@your-db-endpoint:5432/your_database'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 데이터베이스 초기화
    db.init_app(app)

    # 테이블 생성
    @app.before_first_request
    def create_tables():
        db.create_all()

    return app