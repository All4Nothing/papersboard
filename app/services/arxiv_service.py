import requests
import arxiv
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
import logging
import time
from tqdm import tqdm

from app.services.database import db
from app.models import Paper
from app.models.last_update import LastUpdate
from app.services.nlp_service import  summarize_abstract 


logger = logging.getLogger(__name__)

MAX_PAPER_COUNT = 100

BASE_URL = "http://export.arxiv.org/api/query"

ARXIV_CATEGORY_MAPPING = {
    "cs.AI": "Artificial Intelligence",
    "cs.LG": "Machine Learning",
    "cs.CV": "Computer Vision",
    "cs.CL": "Natural Language Processing",
    "cs.RO": "Robotics",
    "cs.NE": "Neural Networks",
    "cs.IR": "Information Retrieval",
    "cs.MA": "Multi-Agent Systems",
    "stat.ML": "Statistical Machine Learning",
}

def categorize_papers(arxiv_categories):
    """
    논문 데이터를 카테고리별로 분류합니다.
    """
    subject_labels = set()

    for category in arxiv_categories.split():
        if category in ARXIV_CATEGORY_MAPPING:
            subject_labels.add(ARXIV_CATEGORY_MAPPING[category])

    return ", ".join(subject_labels) if subject_labels else "Other"

def fetch_and_save_papers():
    """
    Arxiv에서 논문 데이터를 수집하여 데이터베이스에 저장합니다.
    """
    categories = ARXIV_CATEGORY_MAPPING.keys()
    search_query = 'cat:' + ' OR cat:'.join(categories)
    one_week_ago = datetime.now(timezone.utc) - timedelta(days=31)  # UTC 기준 최근 7일

    search = arxiv.Search(
        query=search_query,
        max_results=MAX_PAPER_COUNT,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )

    try:
        time.sleep(3)
        results = list(search.results())  # tqdm을 사용하기 위해 리스트로 변환
        print(f" 🔍 {len(results)} papers found")
        if not results:  # ✅ API 응답이 비어 있는 경우 예외 처리
            print("arXiv에서 가져온 논문이 없습니다. (빈 결과)")
            return

    except arxiv.UnexpectedEmptyPageError:
        print("❌ arXiv API 오류: 빈 페이지가 반환되었습니다. 다시 시도해 주세요.")
        return
    
    added_count = 0
    skipped_count = 0

    print(f"🔍 {len(results)} papers found")

    for result in tqdm(results, desc="Adding papers", unit="paper"):
        time.sleep(3)  # ✅ 요청 속도 제한 추가

        # 날짜를 필터링하여 1주일 이내 데이터만 처리
        if result.published >= one_week_ago:  # aware datetime 비교
            
            existing_paper = Paper.query.filter_by(url=result.entry_id).first()

            if existing_paper:
                print(f"Already existed paper : {result.title} (URL: {result.entry_id})")
                skipped_count += 1
                continue

            domain_task = categorize_papers(result.primary_category)
            summary = summarize_abstract(result.summary)

            paper = Paper(
                title=result.title,
                abstract=result.summary,
                authors=', '.join([author.name for author in result.authors]),
                published_date=result.published,
                source='arXiv',
                url=result.entry_id.strip(),
                domain_task=domain_task,
                summary = summary,
            )
            try:
                db.session.add(paper)
                db.session.commit()
                added_count += 1
                print(f"✅ paper added: {result.title}")
                print(f"summary: {summary}")
    
            except Exception as e:
                print(f"❌ paper add failed: {result.title} (error: {str(e)})")
                db.session.rollback()
    
    # latest update time update
    try:
        print("🕒 Updating last_update timestamp")
        db.session.query(LastUpdate).delete()
        db.session.add(LastUpdate(updated_at=datetime.now()))
        print(f"✅ Last update timestamp updated: {datetime.now()}")
    except Exception as e:
        print(f"❌ Last update timestamp update failed: {str(e)}")
        db.session.rollback()

    db.session.commit()
    print(f"✅ {added_count} papers are added")
    print(f"❌ {skipped_count} papers are skipped")

    # delete old papers
    clean_old_papers()

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

def clean_old_papers():
    """
    Delete old papers from the database
    """
    total_papers = Paper.query.count()

    if total_papers > MAX_PAPER_COUNT:
        num_to_delete = total_papers - MAX_PAPER_COUNT
        old_papers = Paper.query.order_by(Paper.published_date.asc()).limit(num_to_delete).all()

        for paper in old_papers:
            db.session.delete(paper)
        db.session.commit()

        print(f"✅ {num_to_delete} papers are deleted. {MAX_PAPER_COUNT} papers are remained.")
