import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
import logging

logger = logging.getLogger(__name__)

BASE_URL = "http://export.arxiv.org/api/query"

def fetch_latest_papers(query="artificial intelligence", max_results=50, last_days=None):
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
        return []

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