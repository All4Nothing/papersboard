from flask import Flask
from flask_cors import CORS
from transformers import pipeline
from apscheduler.schedulers.background import BackgroundScheduler
from flask_sqlalchemy import SQLAlchemy
from pytz import utc
from flask_migrate import Migrate

from app.routes.main_routes import main_routes
from app.routes.paper_routes import paper_routes
from app.routes import register_blueprints
from app.services import initialize_services
from app.services.arxiv_service import fetch_and_save_papers
from app.services.database import db

import os
import logging

def create_app():
    app = Flask(__name__, template_folder=os.path.join("app", "templates"))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yongjoo:ghsekrhfh56!@papersboard.cho0qeuiuv8z.ap-northeast-2.rds.amazonaws.com:5432/papersdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 데이터베이스 초기화
    db.init_app(app)

    # 테이블 생성
    @app.before_request
    def initialize_database():
        """
        첫 번째 요청 전에 데이터베이스 테이블을 초기화합니다.
        """
        with app.app_context():
            db.create_all()

    # 블루프린트 등록
    app.register_blueprint(main_routes, url_prefix='/api')
    app.register_blueprint(paper_routes, url_prefix="/papers")
    

    return app


def initialize_scheduler():
    """
    논문 데이터를 매일 수집하기 위한 스케줄러를 설정합니다.
    """
    scheduler = BackgroundScheduler(timezone=utc)  # pytz.timezone 객체 사용
    scheduler.add_job(func=fetch_and_save_papers, trigger='interval', days=1)
    scheduler.start()

# Flask 애플리케이션 실행
if __name__ == "__main__":
    app = create_app()
    migrate = Migrate(app, db)
    initialize_scheduler()
    app.run(debug=True)