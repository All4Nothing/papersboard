import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.services.arxiv_service import fetch_and_save_papers

app = create_app()

with app.app_context():
    fetch_and_save_papers()
    print("Fetch Papers Completed")