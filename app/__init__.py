from flask import Flask
from app.services.database import db
from flask_migrate import Migrate
from app.routes import register_blueprints
import os

# 🔹 Paper 모델을 강제로 로드하여 Flask-Migrate가 감지할 수 있도록 함
from app.models.paper import Paper

migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # 📌 SQLite 데이터베이스 절대 경로 설정 (파일이 생성되는 위치를 명확히 하기 위해)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # 현재 파일의 디렉토리 경로
    DB_PATH = os.path.join(BASE_DIR, 'papers.db')  # 절대 경로로 설정

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 데이터베이스 초기화
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        print("Create DB")  
        print(f"DB path: {DB_PATH}")
        db.create_all() 
    
    register_blueprints(app)
    
    return app

'''PostgreSQL
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
    
    return app'''