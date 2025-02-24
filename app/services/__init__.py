from .arxiv_service import fetch_and_save_papers
from .data_processing import process_paper_data

def initialize_services(app):
    app.logger.info("Services initialized successfully.")