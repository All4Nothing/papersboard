from flask import Blueprint, render_template, request, jsonify
from app.services.database import db
from app.models.paper import Paper
from app.services.nlp_service import classify_domain_task_with_model
from app.models.last_update import LastUpdate

main_routes = Blueprint("main_routes_", __name__, url_prefix='/api')

# 메인 페이지
@main_routes.route("/")
def index():
    """
    메인 페이지: 데이터베이스에서 최신 논문을 가져와 렌더링합니다.
    """
    categories = ["cs.AI", "cs.LG", "cs.CV", "stat.ML"]  # 딥러닝 관련 카테고리
    papers = Paper.query.order_by(Paper.published_date.desc()).limit(20).all()
    # category_counts 계산 (필수)
    category_counts = {}
    for category in categories:
        count = Paper.query.filter_by(source=category).count()
        category_counts[category] = count

    selected_category = request.args.get("category")  # 사용자가 선택한 카테고리

    if selected_category:
        papers = Paper.query.filter(Paper.source == selected_category).order_by(Paper.published_date.desc()).all()
    else:
        papers = Paper.query.order_by(Paper.published_date.desc()).limit(20).all()  # 최근 20개 논문

    return render_template("index.html", papers=papers, category_counts=category_counts)

# 논문 데이터 JSON 반환
@main_routes.route("/api/papers", methods=["GET"])
def get_papers():
    """
    논문 데이터를 JSON 형식으로 반환합니다.
    """
    category = request.args.get("category")

    # 🔍 디버깅 로그 추가
    print(f"🔍 요청된 카테고리: {category}")

    if category:
        # `domain_task` 컬럼을 사용해 필터링하도록 수정
        papers = Paper.query.filter(Paper.domain_task == category).order_by(Paper.published_date.desc()).all()
    else:
        papers = Paper.query.order_by(Paper.published_date.desc()).limit(20).all()

    # 🔍 API 응답 확인
    print(f"📄 반환된 논문 수: {len(papers)}")

    papers_data = [
        {
            "title": paper.title,
            "abstract": paper.abstract,
            "authors": paper.authors,
            "published_date": paper.published_date.strftime("%Y-%m-%d"),
            "url": paper.url,
            "domain_task": paper.domain_task,
        }
        for paper in papers
    ]

    return jsonify(papers_data)

# 논문 검색 기능
@main_routes.route("/search", methods=["GET"])
def search_papers():
    """
    제목이나 초록으로 논문을 검색합니다.
    """
    query = request.args.get("q")
    if query:
        papers = Paper.query.filter(
            (Paper.title.ilike(f"%{query}%")) | (Paper.abstract.ilike(f"%{query}%"))
        ).order_by(Paper.published_date.desc()).all()
    else:
        papers = []

    return render_template("search_results.html", papers=papers)

@main_routes.route('/classify', methods=['POST'])
def classify_paper():
    """논문 제목과 초록을 기반으로 Domain Task를 분류하는 API."""
    data = request.json
    title = data.get("title", "")
    abstract = data.get("abstract", "")

    task = classify_domain_task_with_model(title, abstract)
    return jsonify({"domain_task": task})

@main_routes.route('/api/category_counts', methods=['GET'])
def get_category_counts():
    """
    카테고리별 논문 수를 반환하는 API
    """
    category_counts = (
        db.session.query(Paper.domain_task, db.func.count(Paper.id))
        .group_by(Paper.domain_task)
        .all()
    )
    
    # 디버깅용 출력
    print("Category Counts Raw Result:", category_counts)

    # 데이터를 JSON 형식으로 반환
    response = {category: count for category, count in category_counts}
    return jsonify(response)

@main_routes.route('/api/last_update', methods=['GET'])
def get_last_update():
    """
    return last update time in JSON format
    """
    last_update = LastUpdate.query.order_by(LastUpdate.updated_at.desc()).first()
    if last_update:
        return jsonify({"last_update": last_update.updated_at.strftime("%Y-%m-%d %H:%M:%S UTC")})
    else:
        return jsonify({"last_update": None})
    
@main_routes.route("/api/all_papers", methods=["GET"])
def get_all_papers():
    """
    각 카테고리별 논문 리스트를 반환하는 API.
    """
    categories = ["Computer Vision", "Natural Language Processing", "Recommendation System", "Reinforcement Learning"]
    papers_by_category = {}

    for category in categories:
        papers = Paper.query.filter_by(domain_task=category).order_by(Paper.published_date.desc()).limit(100).all()
        papers_by_category[category] = [
            {
                "title": paper.title,
                "abstract": paper.abstract,
                "summary": paper.summary,
                "authors": paper.authors,
                "published_date": paper.published_date.strftime("%Y-%m-%d"),
                "url": paper.url,
                "keywords": paper.keywords 
            }
            for paper in papers
        ]

    return jsonify(papers_by_category)