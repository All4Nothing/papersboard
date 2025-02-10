from flask import Flask
from flask_cors import CORS
from transformers import pipeline
from apscheduler.schedulers.background import BackgroundScheduler
from flask_sqlalchemy import SQLAlchemy
from pytz import utc
from flask_migrate import Migrate

from app import create_app, db
from app.routes.main_routes import main_routes
from app.routes.paper_routes import paper_routes
from app.routes import register_blueprints
from app.services import initialize_services
from app.services.arxiv_service import fetch_and_save_papers
from app.services.database import db

import os
import logging

app = create_app()

def initialize_scheduler():
    """
    논문 데이터를 매일 수집하기 위한 스케줄러를 설정합니다.
    """
    scheduler = BackgroundScheduler(timezone=utc)  # pytz.timezone 객체 사용
    scheduler.add_job(func=fetch_and_save_papers, trigger='interval', days=1)
    scheduler.start()

# Flask 애플리케이션 실행
if __name__ == "__main__":
    initialize_scheduler()
    app.run(debug=True)                                                                                   