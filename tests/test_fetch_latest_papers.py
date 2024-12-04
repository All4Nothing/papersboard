import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 이제 절대 경로로 가져오기
from app.services.arxiv_service import fetch_latest_papers

if __name__ == "__main__":
    # "Reinforcement Learning"과 관련된 논문 10개 가져오기
    papers = fetch_latest_papers("Reinforcement Learning", max_results=10)
    print(papers)  # 반환된 데이터를 출력하여 확인