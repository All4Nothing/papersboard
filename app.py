from flask import Flask
from flask_cors import CORS
from transformers import pipeline
from apscheduler.schedulers.background import BackgroundScheduler
from flask_sqlalchemy import SQLAlchemy

from app.routes.main_routes import main_routes
from app.routes.paper_routes import paper_routes
from app.routes import register_blueprints
from app.services import initialize_services
from app.services.arxiv_service import fetch_and_save_papers

import os
import logging

app = Flask(__name__, template_folder=os.path.join("app", "templates"))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yongjoo:Ghsekrhfh56!@aipapers.cho0qeuiuv8z.ap-northeast-2.rds.amazonaws.com:5432/aipapers'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


CORS(app)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

register_blueprints(app)
initialize_services(app)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=fetch_and_save_papers, trigger="interval", days=1)
    scheduler.start()

if __name__ == "__main__":
    start_scheduler()
    app.run(debug=True)