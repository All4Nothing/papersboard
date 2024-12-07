import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from app.database import save_paper_to_db
import logging

logger = logging.getLogger(__name__)

BASE_URL = "http://export.arxiv.org/api/query"

def categorize_papers(papers):
    """
    논문 데이터를 카테고리별로 분류합니다.
    """
    category_counts = {}
    for paper in papers:
        categories = paper.get("categories", "").split()
        for category in categories:
            category_counts[category] = category_counts.get(category, 0) + 1
    return category_counts

def fetch_and_save_papers():
    """
    Arxiv API에서 논문 데이터를 가져와 데이터베이스에 저장합니다.
    """
    # 최근 7일 이내 제출된 논문
    one_week_ago = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
    query = "cat:cs.AI OR cat:cs.LG OR cat:cs.CV OR cat:stat.ML"
    
    params = {
        "search_query": f"{query} AND submittedDate:[{one_week_ago} TO *]",
        "start": 0,
        "max_results": 200,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }

    # Arxiv API 호출
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        print(f"Error fetching papers from Arxiv: {response.status_code}")
        return

    # XML 응답 파싱
    papers = parse_arxiv_response(response.text)
    for paper in papers:
        save_paper_to_db(paper)  # 데이터베이스에 저장
    print(f"{len(papers)} papers saved to the database.")


def parse_arxiv_response(xml_data):
    """
    arXiv API 응답 XML 데이터를 파싱하여 논문 제목과 초록을 추출합니다.
    """
    root = ET.fromstring(xml_data)
    papers = []

    for paper in papers:
        logger.info(f"불러온 논문 제목: {paper['title']}")

    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = entry.find("{http://www.w3.org/2005/Atom}title").text
        summary = entry.find("{http://www.w3.org/2005/Atom}summary").text
        papers.append({"title": title.strip(), "abstract": summary.strip()})

    return papers

'''def fetch_latest_papers(query="artificial intelligence", max_results=50, last_days=None):
    """
    arXiv에서 최신 논문 데이터를 가져옵니다. 
    날짜 필터링 기능이 추가되었습니다.

    Args:
        query (str): 검색할 쿼리.
        max_results (int): 최대 논문 개수.
        last_days (int, optional): 최근 몇 일 동안의 데이터를 가져올지.

    Returns:
        list: 논문 리스트.
    """
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }

    # 날짜 필터링
    if last_days:
        # 현재 UTC 시간에서 last_days만큼 이전의 날짜 계산
        start_date = (datetime.now(timezone.utc) - timedelta(days=last_days)).strftime('%Y%m%d%H%M%S')
        # submittedDate 필드를 사용하여 날짜 범위 지정
        params["search_query"] += f" AND submittedDate:[{start_date} TO *]"

    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return parse_arxiv_response(response.text)
    else:
        return []'''