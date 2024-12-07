# 서비스 모듈 임포트
from .arxiv_service import fetch_and_save_papers
from .data_processing import process_paper_data
from .recommendation import recommend_papers

# 서비스 초기화 및 로깅 설정이 필요할 경우 추가 가능
def initialize_services(app):
    """
    서비스 초기화 로직을 포함합니다. Flask 앱 컨텍스트와 함께 동작하도록 설정.
    """
    app.logger.info("Services initialized successfully.")