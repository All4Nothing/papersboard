from flask import Blueprint, render_template, request, jsonify
from app.services.database import db
from app.models.paper import Paper
from app.models.last_update import LastUpdate

main_routes = Blueprint("main_routes_", __name__, url_prefix='/api')

@main_routes.route("/")
def index():
    categories = ["cs.AI", "cs.LG", "cs.CV", "stat.ML"]
    papers = Paper.query.order_by(Paper.published_date.desc()).limit(20).all()
    category_counts = {}
    for category in categories:
        count = Paper.query.filter_by(source=category).count()
        category_counts[category] = count

    selected_category = request.args.get("category")

    if selected_category:
        papers = Paper.query.filter(Paper.source == selected_category).order_by(Paper.published_date.desc()).all()
    else:
        papers = Paper.query.order_by(Paper.published_date.desc()).limit(20).all()

    return render_template("index.html", papers=papers, category_counts=category_counts)

@main_routes.route("/search", methods=["GET"])
def search_papers():
    query = request.args.get("q")
    if query:
        papers = Paper.query.filter(
            (Paper.title.ilike(f"%{query}%")) | (Paper.abstract.ilike(f"%{query}%"))
        ).order_by(Paper.published_date.desc()).all()
    else:
        papers = []

    return render_template("search_results.html", papers=papers)

@main_routes.route('/api/category_counts', methods=['GET'])
def get_category_counts():
    category_counts = (
        db.session.query(Paper.domain_task, db.func.count(Paper.id))
        .group_by(Paper.domain_task)
        .all()
    )
    
    print("Category Counts Raw Result:", category_counts)

    response = {category: count for category, count in category_counts}
    return jsonify(response)

@main_routes.route('/api/last_update', methods=['GET'])
def get_last_update():
    last_update = LastUpdate.query.order_by(LastUpdate.updated_at.desc()).first()
    if last_update:
        return jsonify({"last_update": last_update.updated_at.strftime("%Y-%m-%d %H:%M:%S UTC")})
    else:
        return jsonify({"last_update": None})
    
@main_routes.route("/api/all_papers", methods=["GET"])
def get_all_papers():
    categories = ["Artificial Intelligence",
    "Machine Learning",
    "Computer Vision",
    "Natural Language Processing",
    "Robotics",
    "Neural Networks",
    "Information Retrieval",
    "Multi-Agent Systems",
    "Statistical Machine Learning"]
    
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
            }
            for paper in papers
        ]

    return jsonify(papers_by_category)