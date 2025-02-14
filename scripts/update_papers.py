import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.services.arxiv_service import update_missing_paper_data

app = create_app()

with app.app_context():
    update_missing_paper_data()
    print("Update Papers Completed")