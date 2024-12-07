from flask import Blueprint, request, jsonify
from app.services.database import db, Paper

paper_routes = Blueprint("paper_routes", __name__)

# 특정 논문 세부 정보 API
@paper_routes.route("/api/paper/<int:paper_id>", methods=["GET"])
def get_paper(paper_id):
    """
    특정 논문의 세부 정보를 JSON 형식으로 반환합니다.
    """
    paper = Paper.query.get(paper_id)
    if not paper:
        return jsonify({"error": "Paper not found"}), 404

    paper_data = {
        "title": paper.title,
        "abstract": paper.abstract,
        "authors": paper.authors,
        "published_date": paper.published_date.strftime("%Y-%m-%d"),
        "url": paper.url,
        "source": paper.source,
    }
    return jsonify(paper_data)

# 모든 논문 목록 API
@paper_routes.route("/api/papers", methods=["GET"])
def get_all_papers():
    """
    모든 논문의 목록을 JSON 형식으로 반환합니다.
    """
    category = request.args.get("category")
    limit = int(request.args.get("limit", 20))  # 기본적으로 20개 제한
    query = Paper.query

    if category:
        query = query.filter(Paper.source == category)

    papers = query.order_by(Paper.published_date.desc()).limit(limit).all()

    papers_data = [
        {
            "id": paper.id,
            "title": paper.title,
            "abstract": paper.abstract,
            "authors": paper.authors,
            "published_date": paper.published_date.strftime("%Y-%m-%d"),
            "url": paper.url,
        }
        for paper in papers
    ]
    return jsonify(papers_data)

# 논문 삭제 API
@paper_routes.route("/api/paper/<int:paper_id>", methods=["DELETE"])
def delete_paper(paper_id):
    """
    특정 논문을 삭제합니다.
    """
    paper = Paper.query.get(paper_id)
    if not paper:
        return jsonify({"error": "Paper not found"}), 404

    db.session.delete(paper)
    db.session.commit()
    return jsonify({"message": f"Paper with ID {paper_id} has been deleted."})

# 논문 추가 API
@paper_routes.route("/api/paper", methods=["POST"])
def add_paper():
    """
    새 논문 데이터를 추가합니다.
    """
    data = request.json
    required_fields = ["title", "abstract", "authors", "published_date", "url", "source"]

    # 필수 필드 확인
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    paper = Paper(
        title=data["title"],
        abstract=data["abstract"],
        authors=data["authors"],
        published_date=data["published_date"],
        url=data["url"],
        source=data["source"],
    )

    db.session.add(paper)
    db.session.commit()
    return jsonify({"message": "Paper added successfully.", "paper_id": paper.id}), 201