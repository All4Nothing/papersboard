from flask import Blueprint, jsonify
from app.services.arxiv_service import fetch_latest_papers

paper_routes = Blueprint("paper_routes", __name__)

@paper_routes.route("/latest")
def latest_papers():
    papers = fetch_latest_papers()
    return jsonify(papers)