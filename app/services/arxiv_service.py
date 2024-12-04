import requests
import xml.etree.ElementTree as ET


BASE_URL = "http://export.arxiv.org/api/query"

def fetch_latest_papers(query, max_results=10):
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    print(f"Fetching papers with query: {params['search_query']}")  # 쿼리 출력
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        # XML 데이터를 파싱해서 필요한 정보 추출 (간단화된 처리)
        return {"status": "success", "data": parse_arxiv_response(response.text)}
    else:
        return {"status": "error", "message": "Failed to fetch data"}

def parse_arxiv_response(xml_data):
    """
    arXiv API 응답 XML 데이터를 파싱하여 논문 제목과 초록을 추출합니다.
    """
    root = ET.fromstring(xml_data)
    papers = []

    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = entry.find("{http://www.w3.org/2005/Atom}title").text
        summary = entry.find("{http://www.w3.org/2005/Atom}summary").text
        papers.append({"title": title.strip(), "abstract": summary.strip()})

    return papers