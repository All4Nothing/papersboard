from flask import Flask
from app.services.database import db
from flask_migrate import Migrate

from app.routes import register_blueprints  # Blueprint 등록 함수 가져오기


migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # PostgreSQL 데이터베이스 URI 설정
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yongjoo:ghsekrhfh56!@papersboard.cho0qeuiuv8z.ap-northeast-2.rds.amazonaws.com:5432/papersdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 데이터베이스 초기화
    db.init_app(app)
    migrate.init_app(app ,db)

    # 테이블 생성
    with app.app_context():
        db.create_all()

    register_blueprints(app)
    
    return app